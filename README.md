# 🛸 ArduPilot Companion Monitor & Failsafe System

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![ArduPilot](https://img.shields.io/badge/ArduPilot-SITL-orange.svg)
![MAVLink](https://img.shields.io/badge/MAVLink-2.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

A modular companion computer simulation for ArduPilot SITL. This system monitors real-time hardware health (CPU Load and Temperature) and executes an intelligent **RTL (Return to Launch)** failsafe when critical thresholds are exceeded.

---

## 🧠 System Architecture

The project is built with a modular approach, separating telemetry, safety logic, and logging to ensure high reliability—similar to real-world flight software.

- **`sim_companion.py`**: The central "Brain" that manages MAVLink communication and coordinates mission execution.
- **`failsafe.py`**: The "Safety Officer" that implements temporal filtering (5-second rule) for CPU spikes to prevent false positives.
- **`logger.py`**: The "Black Box" that records high-resolution CSV flight data with unit formatting (°C/%).
- **`stress.py`**: A dedicated testing tool designed to simulate 100% CPU load across all cores to verify failsafe triggers.

---

🏗️ Technical Architecture
This system follows a decoupled watchdog architecture, ensuring that the health monitor operates independently of the flight simulation to provide reliable failsafe triggers.

1. System Flow Overview
The integration consists of three primary layers working in synchronization:

Orchestration Layer (start_sim.sh): A high-level bash controller that initializes the ArduPilot SITL environment, manages MAVProxy port routing, and spawns the background monitoring processes.

Monitoring Layer (failsafe.py): A Python-based "Watchdog" that taps into the system's hardware via psutil. It evaluates real-time CPU load and thermal metrics against predefined safety thresholds.

Communication Layer (MAVLink): Utilizing pymavlink, the monitor sends heartbeat packets and status updates. When a critical threshold is breached, it issues a MAV_CMD_DO_SET_MODE command to the Flight Controller to trigger an emergency RTL (Return to Launch).

2. Logic & Data Flow
graph TD
    A[start_sim.sh] --> B[SITL Flight Controller]
    A --> C[Python Health Monitor]
    C -->|GET Hardware Stats| D(CPU/RAM/Temp)
    D -->|Threshold Breach| C
    C -->|MAVLink: SET_MODE RTL| B
    C -->|Log Data| E[(flight_data.csv)]

3. Superior Reliability Features
Unlike standard monitoring scripts, this implementation features:

Asynchronous Logging: Telemetry recording to flight_data.csv happens non-blockingly, ensuring that disk I/O latency never delays a critical failsafe command.

Automated Environmental Setup: The bash script handles the heavy lifting of port mapping (127.0.0.1:14550), meaning the user never has to manually "handshake" the companion computer with the drone.

Stress-Test Ready: Includes a stress.py utility to intentionally spike system load, allowing for deterministic verification of the failsafe logic without risking physical hardware.



Data Acquisition: sim_companion.py uses the psutil library to poll the host machine's hardware metrics every 1 second.

Monitoring & Logging: These metrics are passed to logger.py, which formats the data with units (°C/%) and appends it to a persistent CSV "Black Box" file.

Safety Evaluation: The FailsafeManager in failsafe.py evaluates the data against predefined thresholds.

Temporal Filtering: To prevent accidental triggers from momentary spikes, the system requires the CPU to remain above the threshold for a continuous 5-second window before acting.

Command Execution: Once the 5-second timer expires, the script sends a MAV_CMD_DO_SET_MODE command via MAVLink to the SITL instance, forcing the drone into RTL (Return to Launch) mode and broadcasting a high-priority warning message.


## ✨ Key Features

- ✅ **Intelligent Failsafe**: Triggers RTL if CPU > 95% for 5+ seconds or Temperature > 75°C.
- ✅ **Automated Deployment**: `start_sim.sh` handles virtual environment setup and ArduPilot SITL launching.
- ✅ **Mission Automation**: Executes flight commands (Mode, Arm, Takeoff) via `my_flight.txt`.
- ✅ **Clean Telemetry**: Sends custom MAVLink `NAMED_VALUE_FLOAT` packets visible in Mission Planner/QGC.
- ✅ **Professional Logging**: Generates `flight_data.csv` with precise timestamps and unit-labeled columns.

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have ArduPilot SITL installed and compiled on your Linux machine.

### 2. Launch the System
Use the automated bash script to setup the environment and start the sitl simulation:
No manual SITL configuration required; the script handles environment variables and port forwarding automatically.
My bash cammand will start the whole system for you no need for manually typing to start sitl simulation  it will manage 
it for you including take off for sitl drone and python mavlink based heart beat telemetry , It will also create csv file that records temperature , cpu power consumption and status as well , best part bash script will handle it for you no need to manually type command for them at all
```bash
chmod +x start_sim.sh
./start_sim.sh
4. Test the Failsafe
To simulate a hardware failure and verify the RTL trigger, run the stress test:

Bash
python stress.py

Timestamp,CPU Load (%),Temperature (°C),System Status
14:20:05,  12.4%,         45.2°C,          NORMAL
14:20:10,  99.1%,         48.5°C,        "<span style=""color:orange"">CPU WARNING</span>"
14:20:15,  99.5%,         51.2°C,          "<span style=""color:red"">FAILSAFE_TRIGGERED</span>"

pymavlink

psutil

ArduPilot SITL
## 🛠️ Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

Install dependencies manually if not using the shell script:

Bash
pip install pymavlink psutil
👨‍💻 Author
Mahad Sultan Chaudhary
This project is demo for gsoc Ardupilot Real-Time Companion-Computer Health Monitoring & Failsafe 2026 compeition

GitHub: @mahadsultanchaudhary
