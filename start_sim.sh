#!/bin/bash

# --- CONFIGURATION ---
VENV_DIR=".venv"
ARDUPILOT_PATH="$HOME/ardupilot" 
QGC_PATH="$HOME/Applications/QGC.AppImage"
# ----------------------

echo "🚀 Starting ArduPilot Integrated Environment..."

# 1. Virtual Environment Check
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv $VENV_DIR
fi
source $VENV_DIR/bin/activate

# 2. Quietly ensure dependencies are there
echo "🛠️ Checking dependencies..."
pip install -q empy==3.3.4 pymavlink psutil pexpect MAVProxy

# 3. Launch QGroundControl in the background
if [ -f "$QGC_PATH" ]; then
    echo "🛰️ Launching QGroundControl..."
    $QGC_PATH > /dev/null 2>&1 &
else
    echo "⚠️ QGC not found at $QGC_PATH. Please check the path."
fi

# 4. Launch SITL with Multi-Output
# --out 127.0.0.1:14550 is for QGC (default)
# --out 127.0.0.1:14551 is for your sim_companion.py
echo "🚁 Launching SITL (Skipping Build)..."
gnome-terminal -- bash -c "
cd $ARDUPILOT_PATH/ArduCopter;
$ARDUPILOT_PATH/Tools/autotest/sim_vehicle.py -N -v ArduCopter --console --map --out 127.0.0.1:14551;
exec bash"

# 5. Wait for SITL to warm up
echo "⏳ Waiting 10s for SITL/MAVProxy to stabilize ports..."
sleep 10

# 6. Launch Companion Script
echo "🤖 Launching Companion Monitor..."
# We use 'python' instead of 'python3' to ensure it uses the active venv
python sim_companion.py

# Keep the main process alive to monitor sub-processes
wait