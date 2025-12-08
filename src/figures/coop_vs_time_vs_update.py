import os
import sys
import json
from matplotlib import pyplot as plt


def find_out_dirs(root_dir) -> list[str]:
    out_dirs: list[str] = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == "out.json":
                out_dirs.append(dirpath)
    return out_dirs


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <directory>")
        sys.exit(1)

    root_directory = sys.argv[1]

    if not os.path.isdir(root_directory):
        print(f"Error: '{root_directory}' is not a directory.")
        sys.exit(1)

    plt.figure()
    plt.xlabel("cooperation ratio")
    plt.ylabel("evacuation time")
    plt.grid(True)
    c_values = ["1", "5", "10", "30", "50"]
    rc_values = ["0.1", "0.2", "0.3",
                 "0.4", "0.5", "0.6", "0.7", "0.8", "0.9"]
    for c in c_values:
        times = []
        for rc in rc_values:
            dir_path = os.path.join(
                root_directory,
                f"static/env1/coop_{rc}/update_{c}/strat_inertia_0.1"
            )
            out_dirs = find_out_dirs(dir_path)
            total_time = 0
            count = len(out_dirs)
            for out_dir in out_dirs:
                json_path = os.path.join(out_dir, "out.json")
                try:
                    with open(json_path, "r") as f:
                        data = json.load(f)
                    total_time += len(data.get("escape_time_history", []))
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Warning: Could not read {json_path}: {e}")
            avg_time = total_time / count if count > 0 else 0
            print(f"c={c}, rc={rc}, avg_time={avg_time}, count={count}")
            times.append(avg_time)
        plt.plot(rc_values, times, marker='o')
    plt.legend([f"c={c}" for c in c_values])
    plt.title(
        "Cooperation Percentage vs Evacuation Time\nfor Different Update Intervals")
    plt.savefig(os.path.join(root_directory, "coop_vs_time_vs_update.png"))
    plt.close()

    print("Plot saved to 'coop_vs_time_vs_update.png'")
