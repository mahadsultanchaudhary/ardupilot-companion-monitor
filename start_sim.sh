#!/bin/bash

# --- CONFIGURATION ---
VENV_DIR=".venv"
ARDUPILOT_PATH="$HOME/ardupilot" 
# ----------------------

# 1. Create/Activate Virtual Environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
fi
source $VENV_DIR/bin/activate

# 2. Install requirements quietly
echo "Checking dependencies..."
pip install -q empy==3.3.4 pymavlink psutil pexpect MAVProxy

# 3. Launch SITL
# -N means NO BUILD (skips the 1406 files compilation)
# -w wipes old parameters (optional, but good for a fresh start)
# -v ArduCopter specifies the vehicle
echo "Launching SITL (Skipping Build)..."
gnome-terminal -- bash -c "
cd $ARDUPILOT_PATH/ArduCopter;
./../Tools/autotest/sim_vehicle.py -N -v ArduCopter --console --map;
exec bash"

# 4. Wait for SITL to be ready
# Since we aren't building, 5 seconds is usually enough
echo "Waiting 5s for SITL to initialize..."
sleep 5

# 5. Launch Companion Script
echo "Launching Companion Script..."
python3 sim_companion.py

# Keep the main process alive
wait