from environment import Environment
from person import MovementStrategy
import sys
from visualization import GenericVisualization, VideoVisualization, JsonVisualization
from simulation import run_simulation


def find_argument_value(arg_name: str, default: str) -> str:
    args = [arg for arg in sys.argv if arg.startswith(f"--{arg_name}=")]
    if args:
        return args[0].split("=")[1]
    return default


def find_movement_strategy_argument() -> MovementStrategy:
    strategy_name = find_argument_value("movement", "momentum")
    if not strategy_name:
        return MovementStrategy.STATIC_FIELD
    strategy_name = strategy_name.lower()
    if strategy_name == "random":
        return MovementStrategy.RANDOM
    elif strategy_name == "momentum":
        return MovementStrategy.STATIC_FIELD_WITH_MOMENTUM
    else:
        return MovementStrategy.STATIC_FIELD


def print_usage():
    args = [
        ["--env=env_name", "the environment to use. should be a .txt file in the environment/ directory"],
        ["--movement=strategy_name",
            'the movement strategy to use. options are "static", "momentum", and "random". default is "momentum"'],
        ["--json=filename", "if provided, exports a JSON file with the evacuation data to the given filename"],
        ["--video=filename",
            "if provided, exports a video of the evacuation to the given filename"],
        ["--fps=number", "the frames per second for the exported video"],
        ["--frames", "if provided, exports individual frames as PNG files in addition to the video"],
        ["--spawn_percent=number", "the percentage of people to spawn in the environment"],
        ["--cooperate_percent=number",
            "the percentage of people that will cooperate at the start of the simulation"],
    ]

    print(f"Usage: python {sys.argv[0]} [options]")
    print("Options:")
    for arg, desc in args:
        print(f"  {arg.ljust(26)} {desc}")


if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        print_usage()
        sys.exit(0)

    movement_strategy = find_movement_strategy_argument()
    env_name = find_argument_value("env", "env1")
    env = Environment(env_name)

    json_filename = find_argument_value("json", "")
    video_filename = find_argument_value("video", "")
    visualizers: list[GenericVisualization] = []
    if video_filename:
        fps_str = find_argument_value("fps", "2")
        fps = int(fps_str) if fps_str else 2
        export_frames = "--frames" in sys.argv
        visualizers.append(VideoVisualization(
            filename=video_filename,
            fps=fps,
            export_frames=export_frames
        ))
    if json_filename:
        visualizers.append(JsonVisualization(
            filename=json_filename,
            environment_name=env_name,
            strategy=movement_strategy))

    spawn_percent = float(find_argument_value("spawn_percent", "0.75"))
    cooperate_percent = float(find_argument_value("cooperate_percent", "0.5"))

    run_simulation(movement_strategy=movement_strategy, env=env,
                   visualizers=visualizers, spawn_percent=spawn_percent,
                   cooperate_percent=cooperate_percent,
                   verbose=True)
