import time

class FailsafeManager:
    def __init__(self, cpu_threshold=95.0, temp_threshold=75.0, duration=5.0):
        self.cpu_threshold = cpu_threshold
        self.temp_threshold = temp_threshold
        self.duration = duration  # How many seconds to wait before acting
        
        # Tracking state
        self.cpu_fail_start_time = None
        self.triggered = False

    def check_system(self, cpu, temp):
        """
        Returns (is_dangerous, reason_string)
        is_dangerous only becomes True after the threshold is exceeded for 'duration' seconds.
        """
        # 1. Handle CPU logic with a timer
        if cpu >= self.cpu_threshold:
            if self.cpu_fail_start_time is None:
                # Problem just started, start the clock
                self.cpu_fail_start_time = time.time()
            
            elapsed = time.time() - self.cpu_fail_start_time
            
            if elapsed >= self.duration:
                return True, f"CRITICAL CPU: {cpu}% for {int(elapsed)}s"
            else:
                return False, f"CPU WARNING: {int(self.duration - elapsed)}s remaining..."
        else:
            # CPU is back to safe levels, reset the timer
            self.cpu_fail_start_time = None

        # 2. Handle Temperature (Instant trigger or could also use a timer)
        if temp > self.temp_threshold:
            return True, f"CRITICAL TEMP: {temp}°C"

        return False, "NORMAL"

    def trigger_rtl(self, master):
        if self.triggered:
            return 
            
        print("\n🚨 FAILSAFE ALERT: Threshold exceeded for 5 seconds!")
        print("Switching to RTL...")
        
        rtl_mode = master.mode_mapping().get('RTL')
        if rtl_mode is not None:
            master.set_mode(rtl_mode)
            self.triggered = True
            
            # Send high-severity message to the Ground Control Station
            master.mav.statustext_send(
                4, # MAV_SEVERITY_CRITICAL
                b"FAILSAFE: CPU OVERLOAD - RTL"
            )