from matplotlib import pyplot as plt
from matplotlib.animation import FFMpegWriter
from matplotlib import animation
import numpy as np
from person import Person, PersonGameState, PersonStrategy
from .generic_visualization import GenericVisualization, StepData
from matplotlib.patches import Rectangle
import os


class FrameData:
    def __init__(self, winners: list[tuple[int, int]], losers: list[tuple[int, int]], img: np.ndarray, escaped_count: int):
        self.winners = winners
        self.losers = losers
        self.img = img
        self.escaped_count = escaped_count


class VideoVisualization(GenericVisualization):
    def __init__(self, filename: str, fps: int, export_frames: bool):
        super().__init__()
        self.filename = filename
        self.fps = fps
        self.frame_data: list[FrameData] = []
        self.export_frames = export_frames
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

    def record_step(self, step_data: StepData):
        super().record_step(step_data)
        winners: list[tuple[int, int]] = []
        losers: list[tuple[int, int]] = []
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
                    img[y, x] = [0, 255, 0] if cell.strategy == PersonStrategy.COOPERATE else [
                        255, 0, 0]  # Green for cooperate, Red for defect
                    if cell.game_state == PersonGameState.WON:
                        winners.append((x, y))
                    elif cell.game_state == PersonGameState.LOST:
                        losers.append((x, y))

        self.frame_data.append(FrameData(
            winners=winners,
            losers=losers,
            img=img,
            escaped_count=escaped_count
        ))

    def export(self, verbose):
        # create an animation of the evacuation process
        fig, ax = plt.subplots()

        half_size = 0.45
        full_size = half_size * 2
        highlight_line_width = 1.5

        # Create animation using precomputed frames
        def update(frame_index: int):
            ax.clear()
            frame_data = self.frame_data[frame_index]
            image = ax.imshow(frame_data.img)
            ax.set_title(
                f'Step {frame_index}, Escaped: {frame_data.escaped_count}')

            # Highlight winners and losers
            for x, y in frame_data.winners:
                ax.add_patch(Rectangle((x - half_size, y - half_size), full_size, full_size, fill=True,
                             edgecolor='green', facecolor='none', linewidth=highlight_line_width))
            for x, y in frame_data.losers:
                ax.add_patch(Rectangle((x - half_size, y - half_size), full_size, full_size, fill=True,
                             edgecolor='red', facecolor='none', linewidth=highlight_line_width))
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
        print("Saved evacuation video to " + self.filename)
