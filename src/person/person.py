import math
import random
from environment import Environment
from math import exp
from sys import float_info
from enum import Enum

FAMILIARITY = 10
beta = 0.0


class MovementStrategy(Enum):
    RANDOM = 1
    STATIC_FIELD = 2


def find_open_adjacent_cells(x: int, y: int, env: Environment) -> list[tuple[int, int]]:
    open_cells = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1)]
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if env.is_walkable(new_x, new_y):
            open_cells.append((new_x, new_y))
    return open_cells

def calculate_move_weight(projected: tuple[int, int], momentum_bonus: float, env: Environment) -> float:
    """
    This is the numerator in equation 2 from the paper
    """
    projected_sf = env.static_field[projected[1]][projected[0]]
    # work around finite max float value
    if projected_sf >= float_info.max:
        return float_info.max
    return exp(FAMILIARITY * projected_sf + beta * momentum_bonus)

def calculate_momentum_bonus(projected: tuple[int, int], momentum: tuple[int, int]) -> float:
    dx, dy = projected
    mx, my = momentum

    if mx == 0 and my == 0:
        return 0.0

    dot = mx*dx + my*dy
    mag_prev = math.sqrt(mx*mx + my*my)
    mag_move = math.sqrt(dx*dx + dy*dy)

    if mag_prev == 0 or mag_move == 0:
        return 0.0

    cos_sim = dot / (mag_prev * mag_move)

    # Map cos_sim [-1..1] → bonus [0..4]
    return (cos_sim + 1) / 2 * 4

def hash_letter_to_color(letter: str) -> list[int]:
    random.seed(ord(letter))
    return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]


class PersonStrategy(Enum):
    COOPERATE = 1
    DEFECT = 2


class PersonGameState(Enum):
    NOT_PLAYED = 1
    WON = 2
    LOST = 3


class Person:
    def __init__(self, x: int, y: int, letter: str, strategy: PersonStrategy, movement_strategy: MovementStrategy):
        self.x = x
        self.y = y
        self.letter = letter
        self.projected_x = 0
        self.projected_y = 0
        self.strategy = movement_strategy
        self.color = hash_letter_to_color(letter)
        self.strategy = strategy
        self.movement_strategy = movement_strategy
        self.game_state = PersonGameState.NOT_PLAYED
        self.momentum = (0, 0)

    # Function for person to decide where they want to move next

    def findProjectedMove(self, env):
        self.game_state = PersonGameState.NOT_PLAYED
        if self.movement_strategy == MovementStrategy.RANDOM:
            self._findProjectedMoveRandom(env)
        elif self.movement_strategy == MovementStrategy.STATIC_FIELD:
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

    def calculate_momentum_and_weight(self, projected: tuple[int, int], env: Environment):
        dx = projected[0] - self.x
        dy = projected[1] - self.y
        momentum_bonus = calculate_momentum_bonus((dx, dy), self.momentum)
        return calculate_move_weight((self.projected_x, self.projected_y), momentum_bonus, env)

    def _findProjectedMoveStaticField(self, env):
        open_cells = find_open_adjacent_cells(self.x, self.y, env)
        if len(open_cells) == 0:
            self.projected_x = self.x
            self.projected_y = self.y
            return

        move_weights = [self.calculate_momentum_and_weight(cell, env) for cell in open_cells]
        max_scaled = max(move_weights)
        move_weights = [exp(s - max_scaled) for s in move_weights]
        total_weight = sum(move_weights)
        # The denominator in equation 2 from the paper
        probabilities = [weight / total_weight for weight in move_weights]
        move = random.choices(open_cells, weights=probabilities, k=1)[0]
        self.projected_x = move[0]
        self.projected_y = move[1]
        self.momentum = (self.projected_x - self.x,
                         self.projected_y - self.y)

    # Function for person to choose what they will play in the prisoner's dilemma
    # True means cooperate, False means defect
    def playGame(self):
        if self.strategy == PersonStrategy.COOPERATE:
            return True
        elif self.strategy == PersonStrategy.DEFECT:
            return False
        else:
            raise ValueError("Unknown person strategy")

    def win(self):
        self.game_state = PersonGameState.WON

    def lose(self, num_conflicts, num_cooperators):
        self.game_state = PersonGameState.LOST
        self.projected_x = self.x
        self.projected_y = self.y
        self.momentum = (0, 0)

        # Calculate expected payoff for current strategy and the opposite strategy
        current_strat_payoff = 0.0
        opposite_strat_payoff = 0.0
        if num_conflicts == num_cooperators:
            if self.strategy == PersonStrategy.COOPERATE:
                current_strat_payoff = 1/num_cooperators
                opposite_strat_payoff = 1.0
            elif self.strategy == PersonStrategy.DEFECT:
                current_strat_payoff = 1.0
                opposite_strat_payoff = 1/num_cooperators
        elif num_conflicts - num_cooperators > 1:
            if self.strategy == PersonStrategy.COOPERATE:
                current_strat_payoff = 0.0
                opposite_strat_payoff = 1/((num_conflicts - num_cooperators) ** 2)
            if self.strategy == PersonStrategy.DEFECT:
                current_strat_payoff = 1/((num_conflicts - num_cooperators) ** 2)
                opposite_strat_payoff = 0.0
        # Calculate probability of changing strategy
        # TODO: Might want to add a command line argument to change inertia value
        inertia = 2
        current_strat_payoff = inertia * current_strat_payoff
        probability = 1/(1 + exp((current_strat_payoff - opposite_strat_payoff)/0.1))
        # Change strat if greater than threshold
        # TODO: I'm not sure if the paper specifies a threshold. We may have to change this
        if probability >= 0.5:
            if self.strategy == PersonStrategy.COOPERATE:
                self.strategy = PersonStrategy.DEFECT
            elif self.strategy == PersonStrategy.DEFECT:
                self.strategy = PersonStrategy.COOPERATE

    def __str__(self):
        return self.letter
