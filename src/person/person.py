import random
from environment import Environment
from math import exp
from sys import float_info
from enum import Enum

FAMILIARITY = 10


class MovementStrategy(Enum):
    RANDOM = 1
    STATIC_FIELD = 2


def find_open_adjacent_cells(x: int, y: int, env: Environment) -> list[tuple[int, int]]:
    open_cells = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if env.is_walkable(new_x, new_y):
            open_cells.append((new_x, new_y))
    return open_cells


def calculate_move_weight(projected: tuple[int, int], env: Environment) -> float:
    """
    This is the numerator in equation 2 from the paper
    """
    projected_sf = env.static_field[projected[1]][projected[0]]
    # work around finite max float value
    if projected_sf >= float_info.max:
        return float_info.max
    return exp(FAMILIARITY * projected_sf)


def hash_letter_to_color(letter: str) -> list[int]:
    random.seed(ord(letter))
    return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]


class Person:
    def __init__(self, x, y, letter, strategy=MovementStrategy.STATIC_FIELD):
        self.x = x
        self.y = y
        self.letter = letter
        self.projected_x = 0
        self.projected_y = 0
        self.strategy = strategy
        self.color = hash_letter_to_color(letter)

    # Function for person to decide where they want to move next
    def findProjectedMove(self, env):
        if self.strategy == MovementStrategy.RANDOM:
            self._findProjectedMoveRandom(env)
        elif self.strategy == MovementStrategy.STATIC_FIELD:
            self._findProjectedMoveStaticField(env)
        else:
            raise ValueError("Unknown movement strategy")

    def _findProjectedMoveRandom(self, env):
        open_cells = find_open_adjacent_cells(self.x, self.y, env)
        if len(open_cells) == 0:
            self.projected_x = self.x
            self.projected_y = self.y
            return
        move = random.choice(open_cells)
        self.projected_x = move[0]
        self.projected_y = move[1]

    def _findProjectedMoveStaticField(self, env):
        open_cells = find_open_adjacent_cells(self.x, self.y, env)
        if len(open_cells) == 0:
            self.projected_x = self.x
            self.projected_y = self.y
            return

        move_weights = [calculate_move_weight(
            cell, env) for cell in open_cells]
        total_weight = sum(move_weights)
        # The denominator in equation 2 from the paper
        probabilities = [weight / total_weight for weight in move_weights]
        move = random.choices(open_cells, weights=probabilities, k=1)[0]
        self.projected_x = move[0]
        self.projected_y = move[1]

    # Function for person to choose what they will play in the prisoner's dilemma
    # True means cooperate, False means defect
    def playGame(self):
        # return false 1/4 time
        return random.random() < 0.75

    def win(self):
        pass

    def lose(self):
        self.projected_x = self.x
        self.projected_y = self.y

    def __str__(self):
        return self.letter
