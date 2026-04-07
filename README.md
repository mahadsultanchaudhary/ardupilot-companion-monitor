# 🚀 ArduPilot Companion Monitor & Failsafe

A lightweight **companion-computer simulation for ArduPilot SITL** that monitors system health in real time and triggers an intelligent **RTL (Return to Launch) failsafe** on critical failures.

Designed to demonstrate **failure detection, safety-first response, and reproducible testing** in a simulated drone environment.

---

# 🎥 Demo

## 🖥️ Headless Mode (Automated Test) — Recommended

👉 https://www.youtube.com/watch?v=w2EBA-WCLeo

* Fully terminal-based execution
* Automated CPU stress testing (no manual input)
* Real-time telemetry output
* Automatic RTL trigger after threshold breach

---

## 🗺️ SITL Map Mode (Manual Demo)

👉 https://www.youtube.com/watch?v=oF1YrD4H06A

* Visual SITL map interaction
* MAVLink communication established
* Manual stress testing
* Observable RTL behavior in simulation

---

# ⚙️ Features

* ✅ **Real-Time CPU Monitoring** (1-second interval)
* ⚠️ **Warning System** → triggers at 3 seconds of sustained high CPU
* 🚨 **Failsafe RTL Trigger** → activates at 5 seconds
* 🛡️ **Watchdog Protection** → detects telemetry loss
* 📟 **Headless Mode (Default)** → fully terminal-based operation
* 🗺️ **Optional SITL Map Visualization**
* 🎮 **Optional GCS Integration (QGC)**
* 🤖 **Automated Stress Testing** (no manual triggering required)
* 📄 **CSV Logging with Rotation** (auto-manages file size)

---

# 🧠 System Logic

The system follows a **safety-first monitoring approach**:

### CPU-Based Failsafe

* CPU > threshold detected
* **3 seconds** → Warning issued
* **5 seconds** → RTL command triggered

---

### Telemetry Watchdog

* No telemetry for defined duration
* System assumes companion failure
* RTL is triggered immediately
* Recovery mechanisms can restart monitoring

---

# 🏗️ Architecture Overview

```text
start_sim.sh  →  SITL + Companion Script
                        ↓
               System Monitoring (CPU / Telemetry)
                        ↓
                 Watchdog Evaluation
                        ↓
               MAVLink Command (RTL)
                        ↓
                 Logging (CSV + Terminal)
```

---

# 🖥️ Running the Project

## Default (Headless Mode)

```bash
./start_sim.sh
```

---

## Advanced Modes

### 🗺️ With SITL Map

```bash
./start_sim.sh --map
```

---

### 🎮 With Ground Control (QGC)

```bash
./start_sim.sh --qgc
```

---

### ⚡ With Automated Stress Test

```bash
./start_sim.sh --stress
```

---

### 🗺️ Map + Stress Test

```bash
./start_sim.sh --map --stress
```

---

### 🎮 QGC + Stress Test

```bash
./start_sim.sh --qgc --stress
```

---

### 🔥 Full Mode (Everything Enabled)

```bash
./start_sim.sh --fullmode
```

Includes:

* SITL Map
* QGC
* Automated Stress Testing

---

# 🧪 Testing

## Automated Stress Testing

The system can simulate **100% CPU load automatically**, triggering failsafe behavior without manual input.

This allows:

* deterministic testing
* repeatable results
* reliable demonstration of RTL logic

---

## Manual Stress Testing (Legacy Demo)

```bash
python stress.py
```

Used in earlier demo version for manual validation.

---

# 📊 Logging System

* Logs stored in `flight_data.csv`
* Records:

  * timestamp
  * CPU usage
  * system status

---

## 🔁 Log Rotation

* When file size exceeds **~5MB**:

  * new log file is created
  * older logs are removed

👉 Ensures:

* long-running stability
* no storage overflow

---

# 📟 Headless Mode Output

Real-time terminal output includes:

* CPU usage updates
* Warning states
* Failsafe triggers
* MAVLink communication status

Example:

```
[INFO] CPU: 96%
[WARNING] High CPU detected (3s)
[CRITICAL] Threshold exceeded (5s)
[ACTION] RTL Triggered
```

---

# 🎯 Project Goals

* Simulate **companion-computer behavior** in drones
* Demonstrate **failure detection and recovery**
* Provide a **reproducible testing environment**
* Bridge gap between **simulation and real deployment systems**

---

# 🔮 Future Improvements

* Systemd-based deployment for real companion computers
* Monitoring additional metrics (RAM, Disk, Temperature)
* MAVLink reconnection and recovery logic
* Multi-condition failsafe system
* Hardware integration (Raspberry Pi / Jetson)

---

# 👨‍💻 Author

**Mahad Sultan Chaudhary**
GSoC 2026 Applicant – ArduPilot

---

# ⭐ Final Note

This project focuses on **reliability, safety, and automation**, demonstrating how a companion computer can detect failures and respond intelligently in real-time.

---

