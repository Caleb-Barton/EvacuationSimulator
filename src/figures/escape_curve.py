import os
import sys
import json
from matplotlib import pyplot as plt


OVERWRITE = sys.argv.count("--overwrite") > 0
environment = "env4"
max_time = 0


def find_out_dirs(root_dir) -> list[str]:
    out_dirs: list[str] = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == "out.json":
                out_dirs.append(dirpath)
    return out_dirs


def sum_escape_times(root_dir):
    """
    escape_time_history shows the number of people who have escaped at each time step.

    :param root_dir: Description
    """
    print(f"\nProcessing directory: {root_dir}")
    global max_time
    json_files = []

    # Recursively find all JSON files
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".json"):
                json_files.append(os.path.join(dirpath, filename))

    print(f"\nFound {len(json_files)} JSON files in '{root_dir}'.")

    # Sum escape times
    escape_times = []
    for file_path in json_files:
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            if "escape_time_history" in data:
                arr = data["escape_time_history"]
                escape_times.append(arr)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read {file_path}: {e}")

    # Plot a curve of percentage of people escaped over time
    time_steps = {}
    max_escape_time = max([len(arr) for arr in escape_times], default=0)
    total_count = sum(arr[-1] for arr in escape_times)
    for t in range(max_escape_time):
        escaped_count = sum(arr[t] if t < len(arr) else arr[-1]
                            for arr in escape_times)
        time_steps[t] = escaped_count / total_count
    max_time = max(max_time, max_escape_time + 10)
    plt.plot(list(time_steps.keys()), list(time_steps.values()), marker='o')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <directory>")
        sys.exit(1)

    root_directory = sys.argv[1]

    if not os.path.isdir(root_directory):
        print(f"Error: '{root_directory}' is not a directory.")
        sys.exit(1)

    plt.figure()
    sum_escape_times(f"{root_directory}/static")
    sum_escape_times(f"{root_directory}/momentum")
    plt.xlabel("Time Step")
    plt.ylabel("Fraction of People Escaped")
    plt.title(f"Evacuation Curve")
    plt.xlim(0, max_time)
    plt.grid(True)
    plt.legend(["Static Field", "Static Field w/Momentum"])
    plt.savefig(os.path.join(root_directory, "escape_curve.png"))
    plt.close()
