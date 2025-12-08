import os
import time
import subprocess
from itertools import product
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import threading

# --- User parameters ---
NUM_ITERATIONS = 10
OUT_DIR = "out/attempt5"
FPS = 10
SPAWN_PERCENT = 0.75
FRAMES = False
VIDEO = False
MAX_PARALLEL = 8
PYTHON_EXEC = "python"  # path to python interpreter

MOVEMENT = ["momentum", "static"]
ENVIRONMENT = ["env5"]
COOPERATE_PERCENTS = ["0.5"]
UPDATE_INTERVALS = ["5"]
STRATEGY_INERTIA = ["2.0"]

jobs = list(product(
    MOVEMENT, ENVIRONMENT, COOPERATE_PERCENTS, UPDATE_INTERVALS, STRATEGY_INERTIA, range(
        NUM_ITERATIONS)
))

total_sims = len(jobs)
start_time = time.time()
completed = 0
completed_lock = threading.Lock()  # Thread-safe counter


def run_one_sim(movement: str, env: str, coop: str, update: str, inertia: str, iteration: int) -> float:
    global completed, total_sims

    out_dir = os.path.join(
        OUT_DIR, movement, env, f"coop_{coop}",
        f"update_{update}", f"strat_inertia_{inertia}", f"iter_{iteration}"
    )

    json_path = os.path.join(out_dir, "out.json")
    if os.path.exists(json_path):
        with completed_lock:
            total_sims -= 1
        print_eta()
        return 0  # skipped job

    os.makedirs(out_dir, exist_ok=True)
    out_dir = os.path.abspath(out_dir)

    cmd = [
        PYTHON_EXEC, "main.py",
        f"--env={env}",
        f"--movement={movement}",
        f"--json={os.path.join(out_dir, 'out.json')}",
        f"--spawn_percent={SPAWN_PERCENT}",
        f"--cooperate_percent={coop}",
        f"--update_interval={update}",
        f"--strategy_inertia={inertia}",
        f"--seed={random.randint(0, 1_000_000)}"
    ]

    if env.endswith("4") or env.endswith("5"):
        cmd += [f"--familiarity=200"]

    if VIDEO:
        cmd += [
            f"--video={os.path.join(out_dir, 'out.mp4')}",
            f"--fps={FPS}",
            f"--frames={FRAMES}"
        ]

    # write command to a file for debugging
    with open(os.path.join(out_dir, "command.txt"), "w") as f:
        f.write(" ".join(cmd) + "\n")

    start = time.time()
    result = subprocess.run(cmd, capture_output=True)

    if result.returncode != 0:
        raise RuntimeError(
            f"Simulation failed with return code {result.returncode}")

    with completed_lock:
        completed += 1

    print_eta()
    return time.time() - start


def print_eta():
    global completed, total_sims, start_time

    if completed == 0:
        return

    elapsed = time.time() - start_time
    avg_time = elapsed / completed
    remaining = total_sims - completed
    eta_seconds = avg_time * remaining

    h = int(eta_seconds // 3600)
    m = int((eta_seconds % 3600) // 60)
    s = int(eta_seconds % 60)

    progress = (completed * 100) // total_sims
    print(f"[{completed}/{total_sims} - {progress}%] ETA: {h:02d}:{m:02d}:{s:02d}")


def main():
    print(f"Total simulations to run: {total_sims}")
    print(f"Running {MAX_PARALLEL} jobs in parallel\n")

    with ThreadPoolExecutor(max_workers=MAX_PARALLEL) as executor:
        future_to_job = {executor.submit(
            run_one_sim, *job): job for job in jobs}
        for future in as_completed(future_to_job):
            try:
                future.result()  # This will raise any exceptions from the worker
            except Exception as e:
                print(f"Error in job: {e}")

    total_time = time.time() - start_time
    h = int(total_time // 3600)
    m = int((total_time % 3600) // 60)
    s = int(total_time % 60)
    print(f"\nAll simulations complete! Total time: {h:02d}:{m:02d}:{s:02d}")


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    main()
