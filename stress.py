import multiprocessing
import time
import sys

def heavy_computation():
    while True:
        _ = 100 * 100 

def pulse_display(seconds):
    """A cleaner, high-tech pulse monitor instead of a progress bar."""
    start_time = time.time()
    while (time.time() - start_time) < seconds:
        remaining = max(0, seconds - (time.time() - start_time))
        # High-energy status line
        sys.stdout.write(f"\r⚡ [SYSTEM STRESS] ACTIVE CORES: {multiprocessing.cpu_count()} | COOLDOWN IN: {remaining:.1f}s | STATUS: MAX_LOAD ⚡")
        sys.stdout.flush()
        time.sleep(0.1)
    print("\n\n✅ STRESS CYCLE COMPLETE. RELEASING CORES...")

if __name__ == "__main__":
    cores = multiprocessing.cpu_count()
    processes = [multiprocessing.Process(target=heavy_computation, daemon=True) for _ in range(cores)]
    
    for p in processes: p.start()
    pulse_display(7) # 7 second stress
    
    for p in processes: 
        p.terminate()
        p.join()