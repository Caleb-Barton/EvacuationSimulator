from matplotlib import pyplot as plt
from matplotlib.animation import FFMpegWriter
from matplotlib import animation
import numpy as np
from person import Person, PersonGameState, PersonStrategy
from .generic_visualization import GenericVisualization, StepData
from matplotlib.patches import Circle
import os


class FrameData:
    def __init__(self, people: list[tuple[int, int, PersonStrategy]], img: np.ndarray, escaped_count: int,
                 winners: list[tuple[int, int]], losers: list[tuple[int, int]]):
        self.people = people
        self.img = img
        self.escaped_count = escaped_count
        self.winners: list[tuple[int, int]] = winners
        self.losers: list[tuple[int, int]] = losers


class VideoVisualization(GenericVisualization):
    def __init__(self, filename: str, fps: int, export_frames: bool, verbose: bool):
        super().__init__()
        self.filename = filename
        self.fps = fps
        self.frame_data: list[FrameData] = []
        self.export_frames = export_frames
        self.verbose = verbose
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

    def record_step(self, step_data: StepData):
        super().record_step(step_data)
        winners: list[tuple[int, int]] = []
        losers: list[tuple[int, int]] = []
        people: list[tuple[int, int, PersonStrategy]] = []
        escaped_count = len(step_data.escaped_people)
        height = len(step_data.grid_state)
        width = len(step_data.grid_state[0]) if height > 0 else 0
        img = np.zeros((height, width, 3), dtype=np.uint8)

        for y, row in enumerate(step_data.grid_state):
            for x, cell in enumerate(row):
                if cell == ' ' or cell == 'S':
                    img[y, x] = [255, 255, 255]  # White for empty space
                elif cell == '#':
                    img[y, x] = [0, 0, 0]        # Black for obstacles
                elif cell == 'E':
                    img[y, x] = [0, 255, 0]      # Green for exits
                elif isinstance(cell, Person):
                    # White background for person location
                    img[y, x] = [255, 255, 255]
                    people.append((x, y, cell.strategy))
                    if cell.game_state == PersonGameState.WON:
                        winners.append((x, y))
                    elif cell.game_state == PersonGameState.LOST:
                        losers.append((x, y))

        self.frame_data.append(FrameData(
            people=people,
            img=img,
            escaped_count=escaped_count,
            winners=winners,
            losers=losers
        ))
        if self.verbose:
            print(
                f"Recorded frame: {len(self.frame_data) - 2} with {len(winners)} winners and {len(losers)} losers."
            )

    def export(self, verbose):
        # create an animation of the evacuation process
        fig, ax = plt.subplots()
        radius = 0.4
        winner_radius = 0.125
        strategy_indicator_width = 1.0
        x_size = 0.125

        # Create animation using precomputed frames
        def update(frame_index: int):
            ax.clear()
            frame_data = self.frame_data[frame_index]
            image = ax.imshow(frame_data.img)
            ax.set_title(
                f'Step {frame_index}, Escaped: {frame_data.escaped_count}')

            # Draw people as circles
            for x, y, strategy in frame_data.people:
                color = 'green' if strategy == PersonStrategy.COOPERATE else 'red'
                ax.add_patch(Circle((x, y), radius, fill=True,
                                    facecolor=color, edgecolor='none'))

            # Draw small black circles for winners
            for x, y in frame_data.winners:
                ax.add_patch(Circle((x, y), winner_radius, fill=False,
                                    edgecolor='black', linewidth=strategy_indicator_width))

            # Draw X marks for losers
            for x, y in frame_data.losers:
                ax.plot([x - x_size, x + x_size], [y - x_size, y + x_size],
                        color='black', linewidth=strategy_indicator_width)
                ax.plot([x - x_size, x + x_size], [y + x_size, y - x_size],
                        color='black', linewidth=strategy_indicator_width)

            ax.axis('off')
            if self.export_frames:
                plt.savefig(
                    f'{os.path.dirname(self.filename)}/{frame_index:04d}.png')
            return [image]

        interval = 1000 / self.fps
        ani = animation.FuncAnimation(
            fig, update, frames=len(self.frame_data), interval=interval)
        ani.save(self.filename, writer=FFMpegWriter(fps=self.fps))
        plt.close()
        if verbose:
            print("Saved evacuation video to " + self.filename)
