#!/bin/bash

# --- CONFIGURATION ---
VENV_DIR=".venv"
AP_DIR="$HOME/ardupilot" 
QGC_PATH="$HOME/Applications/QGC.AppImage"

# Default Flags (Off)
USE_MAP=""
USE_QGC=false

# Handle Input Arguments
for arg in "$@"; do
    case $arg in
        --map) USE_MAP="--map" ;;
        --qgc) USE_QGC=true ;;
        --fullmode) USE_MAP="--map"; USE_QGC=true ;;
    esac
done
# ----------------------

echo "🚀 Starting ArduPilot Integrated Environment..."
source $VENV_DIR/bin/activate

# 1. Launch QGroundControl if requested
if [ "$USE_QGC" = true ]; then
    if [ -f "$QGC_PATH" ]; then
        echo "🛰️ Launching QGroundControl..."
        $QGC_PATH > /dev/null 2>&1 &
    else
        echo "⚠️ QGC not found at $QGC_PATH"
    fi
fi

# 2. Launch SITL (with or without --map)
echo "🚁 Launching SITL (Map: ${USE_MAP:-OFF})..."
gnome-terminal -- bash -c "cd $AP_DIR/ArduCopter && $AP_DIR/Tools/autotest/sim_vehicle.py -N -v ArduCopter --console $USE_MAP --out 127.0.0.1:14551; exec bash"

# 3. Wait for SITL
echo "⏳ Waiting 15s for SITL..."
sleep 15

# 4. Launch Stress Script in background after a delay (Automated)
# This will wait 124 seconds total (15 SITL + 30 for flight/takeoff and for other ) before starting stress
(sleep 100 && echo "🔥 Starting Automated Stress Test..." && python stress.py) &

# 5. Launch Companion Monitor
echo "🤖 Launching Companion Monitor..."
python sim_companion.py 

wait