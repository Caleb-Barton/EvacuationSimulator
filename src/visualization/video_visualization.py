from matplotlib import pyplot as plt
from matplotlib.animation import FFMpegWriter
from matplotlib import animation
import numpy as np
from person import Person
from .generic_visualization import GenericVisualization


class VideoVisualization(GenericVisualization):
    def __init__(self, filename: str, fps: int):
        super().__init__()
        self.filename = filename
        self.fps = fps

    def export(self):
        # create an animation of the evacuation process
        fig, ax = plt.subplots()

        # Precompute all frames
        precomputed_frames = []
        for step_data in self.history:
            grid = step_data.grid_state
            height = len(grid)
            width = len(grid[0]) if height > 0 else 0

            img = np.zeros((height, width, 3), dtype=np.uint8)

            # Use vectorized operations for faster color assignment
            for y, row in enumerate(grid):
                for x, cell in enumerate(row):
                    if cell == ' ' or cell == 'S':
                        img[y, x] = [255, 255, 255]  # White for empty space
                    elif cell == '#':
                        img[y, x] = [0, 0, 0]        # Black for obstacles
                    elif cell == 'E':
                        img[y, x] = [0, 255, 0]      # Green for exits
                    elif isinstance(cell, Person):
                        img[y, x] = cell.color

            precomputed_frames.append(img)

        # Create animation using precomputed frames
        def update(frame_index):
            ax.clear()
            image = ax.imshow(precomputed_frames[frame_index])
            ax.set_title(
                f'Step {frame_index + 1}, Escaped: {len(self.history[frame_index].escaped_people)}')
            ax.axis('off')
            return [image]

        interval = 1000 / self.fps
        ani = animation.FuncAnimation(
            fig, update, frames=len(precomputed_frames), interval=interval)
        ani.save(self.filename, writer=FFMpegWriter(fps=self.fps))
        plt.close()
