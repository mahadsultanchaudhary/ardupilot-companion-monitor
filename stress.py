import multiprocessing
import time
import sys

def heavy_computation():
    """Tight loop to maximize CPU usage on a single core."""
    try:
        while True:
            _ = 100 * 100 
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    processes = [] 
    
    try:
        print("🚀 CPU Stress Test Initialized.")
        print("Target: Spike CPU to 100% for 10 seconds to test SITL Failsafe.")
        
        # Small delay to ensure the terminal focus is ready
        time.sleep(0.5)

        try:
            # Added a prompt that accepts just 'y' or 'yes'
            user_input = input("\nReady? (Type 'y' or 'yes' to start): ")
            confirmation = user_input.strip().lower()
        except EOFError:
            # This handles cases where the terminal stream is interrupted
            print("\n⚠️ Terminal input interrupted. Please try running the script again.")
            sys.exit(1)
        
        if confirmation not in ['y', 'yes']:
            print(f"❌ Test cancelled. (You typed: '{confirmation}')")
            sys.exit()

        cores = multiprocessing.cpu_count()
        print(f"\n🔥 Spiking {cores} cores... Watch your Companion Script now!")
        
        for _ in range(cores):
            p = multiprocessing.Process(target=heavy_computation)
            p.daemon = True 
            p.start()
            processes.append(p)

        # Countdown timer
        for i in range(10, 0, -1):
            sys.stdout.write(f"\r⏱️ Stressing... {i}s remaining")
            sys.stdout.flush()
            time.sleep(1)

        print("\n\n✅ Time up! Killing stress processes...")

    except KeyboardInterrupt:
        # This only triggers if you EXPLICITLY hit Ctrl+C
        print("\n\n🛑 Manual stop detected. Cleaning up...")
    
    finally:
        for p in processes:
            p.terminate()
            p.join()
        print("❄️ CPU Cooldown complete. System safe.")        