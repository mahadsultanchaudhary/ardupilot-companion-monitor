import multiprocessing
import time
import sys

def heavy_computation():
    """Tight loop to maximize CPU usage."""
    while True:
        _ = 100 * 100 

if __name__ == "__main__":
    processes = [] 
    try:
        cores = multiprocessing.cpu_count()
        print(f"🔥 AUTOMATED TEST: Spiking {cores} cores for 7 seconds...")
        
        for _ in range(cores):
            p = multiprocessing.Process(target=heavy_computation)
            p.daemon = True 
            p.start()
            processes.append(p)

        # Simple wait for 7 seconds
        time.sleep(7)

        print("\n✅ Time up! Killing stress processes...")

    except KeyboardInterrupt:
        print("\n🛑 Manual stop detected.")
    
    finally:
        for p in multiprocessing.active_children():
            p.terminate()
            p.join()
        print("❄️ CPU Cooldown complete.")