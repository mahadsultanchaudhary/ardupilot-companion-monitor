#!/bin/bash

# --- CONFIGURATION ---
VENV_DIR=".venv"
AP_DIR="$HOME/ardupilot" 
QGC_PATH="$HOME/Applications/QGC.AppImage"
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# Default Flags
USE_MAP=""
USE_QGC=false
RUN_STRESS=false

# Handle Input Arguments
for arg in "$@"; do
    case $arg in
        --map) USE_MAP="--map" ;;
        --qgc) USE_QGC=true ;;
        --stress) RUN_STRESS=true ;;
        --fullmode) USE_MAP="--map"; USE_QGC=true; RUN_STRESS=true ;;
    esac
done
# ----------------------

echo "🚀 Starting ArduPilot Integrated Environment..."

# 1. AUTO-SETUP: Handle Virtual Environment & Dependencies
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

if [ -f "requirements.txt" ]; then
    echo "⚙️  Verifying dependencies (pip install)..."
    # --disable-pip-version-check keeps the output clean
    pip install -r requirements.txt --quiet --disable-pip-version-check
else
    echo "⚠️  No requirements.txt found. Skipping auto-install."
fi

# 2. Launch QGroundControl
if [ "$USE_QGC" = true ]; then
    if [ -f "$QGC_PATH" ]; then
        echo "🛰️ Launching QGroundControl..."
        "$QGC_PATH" > /dev/null 2>&1 &
    else
        echo "⚠️ QGC not found at $QGC_PATH"
    fi
fi

# 3. Launch SITL
echo "🚁 Launching SITL (Map: ${USE_MAP:-OFF})..."
gnome-terminal -- bash -c "cd $AP_DIR/ArduCopter && $AP_DIR/Tools/autotest/sim_vehicle.py -N -v ArduCopter --console $USE_MAP --out 127.0.0.1:14551; exec bash"

# 4. Wait for SITL
echo "⏳ Waiting 15s for SITL boot..."
sleep 15

# 5. Conditional Stress Test
if [ "$RUN_STRESS" = true ]; then
    echo "🔥 Stress Test Scheduled: Will activate in ~100s"
    (sleep 100 && echo -e "\n🔥 WARNING: Starting Automated Stress Test..." && python "$SCRIPT_DIR/stress.py") &
else
    echo "🛡️ Stress Test: DISABLED"
fi

# 6. Launch Companion Monitor
echo "🤖 Launching Companion Monitor..."
python "$SCRIPT_DIR/sim_companion.py"

# Cleanup: Kill background stress/QGC if the main monitor is closed
trap "kill 0" EXIT