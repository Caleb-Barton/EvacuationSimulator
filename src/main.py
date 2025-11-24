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


def find_strategy_argument() -> MovementStrategy:
    strategy_name = find_argument_value("strategy", "static")
    if not strategy_name:
        return MovementStrategy.STATIC_FIELD
    strategy_name = strategy_name.lower()
    if strategy_name == "random":
        return MovementStrategy.RANDOM
    else:
        return MovementStrategy.STATIC_FIELD


if __name__ == "__main__":
    strategy = find_strategy_argument()
    env_name = find_argument_value("env", "env1")
    env = Environment(env_name)

    json_filename = find_argument_value("json", "")
    video_filename = find_argument_value("video", "")
    visualizers: list[GenericVisualization] = []
    if video_filename:
        fps_str = find_argument_value("fps", "2")
        fps = int(fps_str) if fps_str else 2
        visualizers.append(VideoVisualization(
            filename=video_filename,
            fps=fps
        ))
    if json_filename:
        visualizers.append(JsonVisualization(
            filename=json_filename,
            environment_name=env_name,
            strategy=strategy))

    spawn_percent = float(find_argument_value("spawn_percent", "0.75"))

    run_simulation(strategy=strategy, env=env,
                   visualizers=visualizers, spawn_percent=spawn_percent, verbose=True)
