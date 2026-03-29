from pymavlink import mavutil
import psutil
import time
import os
from typing import cast

# Import your custom modules
from logger import FlightLogger
from failsafe import FailsafeManager

# --- HELPER FUNCTIONS ---

def get_cpu_temp():
    """Reads the CPU temperature on Linux."""
    temps = psutil.sensors_temperatures()
    for name in ['coretemp', 'cpu_thermal', 'acpitz']:
        if name in temps:
            return temps[name][0].current
    return 0.0

def wait_for_ekf(master):
    print("⏳ Waiting for GPS/EKF to settle...")
    while True:
        msg = master.recv_match(type='EKF_STATUS_REPORT', blocking=True, timeout=1)
        if msg:
            if msg.flags & 512: # EKF_POS_HORIZ_ABS
                print("✅ EKF Ready! GPS Lock acquired.")
                break
        time.sleep(1)

def set_mode(master, mode):
    mode = mode.upper()
    mode_id = master.mode_mapping().get(mode)
    if mode_id is None:
        print(f"❌ Unknown mode: {mode}")
        return
    master.set_mode(mode_id)
    print(f"✅ Mode set to {mode}")

def arm_drone(master):
    print("🚀 Sending Arm command...")
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0, 1, 0, 0, 0, 0, 0, 0
    )
    t_end = time.time() + 10
    while time.time() < t_end:
        if master.motors_armed():
            print("✅ ARMED!")
            return True
        msg = master.recv_match(type='STATUSTEXT', blocking=False)
        if msg: print(f"   💬 ArduPilot: {msg.text}")
        time.sleep(0.5)
    return False

def take_off(master, altitude):
    print(f"🛫 Takeoff initiated: target {altitude}m...")
    master.mav.command_long_send(
        master.target_system, 
        master.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0, 0, 0, 0, 0, 0, 0, altitude
    )
    while True:
        msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        if msg:
            current_alt = msg.relative_alt / 1000.0
            print(f"   Altitude: {current_alt:.1f}m", end='\r')
            if current_alt >= altitude * 0.95:
                print(f"\n✅ Target Altitude Reached!")
                break
        time.sleep(0.2)

# --- MAIN ENGINE ---

# 1. Setup Connection
connection = cast(mavutil.mavfile, mavutil.mavlink_connection('udpin:localhost:14550'))
print("Waiting for SITL heartbeat...")
connection.wait_heartbeat()
print("Connected!")

# 2. Initialize our Portfolio Modules
logger = FlightLogger("flight_data.csv")
safety = FailsafeManager(cpu_threshold=95.0, temp_threshold=75.0)

# 3. Prepare for Flight
connection.recv_match(type='STATUSTEXT', blocking=False) # Clear buffer
wait_for_ekf(connection)

# 4. Execute Mission File (Modified to include logging/safety checks)
mission_file = "my_flight.txt"
if os.path.exists(mission_file):
    print(f"📖 Reading {mission_file}...")
    with open(mission_file, "r") as f:
        for line in f:
            # While processing mission, we should still monitor health
            cpu = psutil.cpu_percent()
            temp = get_cpu_temp()
            logger.log(cpu, temp, "MISSION_ACTIVE")
            
            parts = line.strip().split()
            if not parts: continue
            
            action = parts[0].lower()
            if action == "mode":
                set_mode(connection, parts[1])
            elif action == "arm":
                if not arm_drone(connection):
                    print("Force Arming...")
                    connection.mav.command_long_send(
                        connection.target_system, connection.target_component,
                        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                        0, 1, 21196, 0, 0, 0, 0, 0
                    )
            elif action == "takeoff":
                take_off(connection, float(parts[1]))
            
            time.sleep(1) 
else:
    print(f"⚠️ {mission_file} not found.")

# 5. Continuous Monitoring Loop
print("\n--- Monitoring System Health (Logger & Failsafe Active) ---")
try:
    while True:
        # GATHER DATA
        cpu = psutil.cpu_percent()
        temp = get_cpu_temp()
        
        # LOGIC: Check Failsafe
        is_dangerous, reason = safety.check_system(cpu, temp)
        status = "NORMAL"
        
        if is_dangerous:
            status = "FAILSAFE_TRIGGERED"
            safety.trigger_rtl(connection)
            print(f"\n🔥 {reason}")

        # ACTION: Log to CSV
        logger.log(cpu, temp, status)

        # ACTION: Send Telemetry to ArduPilot
        connection.mav.named_value_float_send(0, b'CPU_LOAD', cpu)
        connection.mav.named_value_float_send(0, b'CPU_TEMP', temp)
        
        print(f"📊 CPU: {cpu}% | Temp: {temp}°C | Status: {status} ", end='\r')
        time.sleep(1)

except KeyboardInterrupt:
    print("\nShutting down companion script...")