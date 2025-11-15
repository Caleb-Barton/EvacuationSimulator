from math import sqrt
from sys import float_info


class Environment:
    def __init__(self, filename):
        self.width = 0
        self.height = 0
        self.grid: list[list[str | object]] = []  # 2D list of cell types
        self.spawn_points: list[tuple[int, int]] = []
        self.exits: list[tuple[int, int]] = []
        self.obstacles: list[tuple[int, int]] = []
        self.static_field: list[list[float]] = []

        self._load_from_file(f'environment/{filename}.txt')

    def _load_from_file(self, filename):
        """Load and parse the environment file"""
        with open(filename, 'r') as f:
            lines = f.readlines()

        # Parse lines, handling comments
        parsed_lines = []
        for line in lines:
            # Remove comments (everything after //)
            if '//' in line:
                line = line.split('//')[0]
            line = line.rstrip('\n')
            if line.strip():
                parsed_lines.append(line)

        if not parsed_lines:
            raise ValueError(
                "Environment file is empty or contains only comments")

        self.height = len(parsed_lines)
        self.width = max(len(line) for line in parsed_lines)
        self.grid = [[' ' for _ in range(self.width)]
                     for _ in range(self.height)]

        for y, line in enumerate(parsed_lines):
            for x, char in enumerate(line):
                self.grid[y][x] = char

                if char == 'S':
                    self.spawn_points.append((x, y))
                elif char == 'E':
                    self.exits.append((x, y))
                elif char == '#':
                    self.obstacles.append((x, y))

        self._init_static_field()

    def _init_static_field(self):
        """Initialize static field for pathfinding"""
        self.static_field = [[-float('inf') for _ in range(self.width)]
                             for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 'E':
                    # The static field at the exit is the maximum float value to essentially force exiting if adjacent
                    self.static_field[y][x] = float_info.max
                elif self.grid[y][x] == '#':
                    # Obstacles are not walkable
                    self.static_field[y][x] = -float('inf')
                else:
                    closest_exit = self.find_closest_exit(x, y)
                    if closest_exit:
                        exit_x, exit_y = closest_exit
                        # Equation 1 from paper
                        self.static_field[y][x] = 1 / sqrt(
                            (exit_x - x) ** 2 + (exit_y - y) ** 2
                        )
                    else:
                        self.static_field[y][x] = -float('inf')

    def get_cell(self, x, y):
        """Get the cell type at position (x, y)"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        else:
            return '#'

    def is_walkable(self, x, y):
        cell_type = self.get_cell(x, y)
        return cell_type in [' ', 'S', 'E']  # All these are walkable

    def find_closest_exit(self, x, y):
        """
        Find the closest exit to the given (x, y) position.
        Uses the number of steps (taxicab geometry) as distance metric.
        """
        min_distance = float('inf')
        closest_exit = None
        for exit_x, exit_y in self.exits:
            distance = abs(exit_x - x) + abs(exit_y - y)
            if distance < min_distance:
                min_distance = distance
                closest_exit = (exit_x, exit_y)
        return closest_exit

    def __str__(self):
        return '\n'.join(
            ''.join(str(cell) for cell in row)
            for row in self.grid
        )
