from person import Person


class Environment:
    def __init__(self, filename):
        self.width = 0
        self.height = 0
        self.grid: list[list[str | Person]] = []  # 2D list of cell types
        self.spawn_points = []
        self.exits = []
        self.obstacles = []

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

    def get_cell(self, x, y):
        """Get the cell type at position (x, y)"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        else:
            return '#'

    def is_walkable(self, x, y):
        cell_type = self.get_cell(x, y)
        return cell_type in [' ', 'S', 'E']  # All these are walkable

    def __str__(self):
        return '\n'.join(
            ''.join(str(cell) for cell in row)
            for row in self.grid
        )
