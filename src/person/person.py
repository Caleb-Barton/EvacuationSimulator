import math
import random
from environment import Environment
from math import exp
from sys import float_info
from enum import Enum


class MovementStrategy(Enum):
    RANDOM = 1
    STATIC_FIELD = 2
    STATIC_FIELD_WITH_MOMENTUM = 3


def calculate_distance(loc_1: tuple[int, int], loc_2: tuple[int, int]) -> float:
    dx = loc_2[0] - loc_1[0]
    dy = loc_2[1] - loc_1[1]
    return math.sqrt(dx*dx + dy*dy)


def find_open_adjacent_cells(x: int, y: int, env: Environment) -> list[tuple[int, int]]:
    open_cells = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                  (1, 1), (1, -1), (-1, -1), (-1, 1)]
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if env.is_walkable(new_x, new_y):
            open_cells.append((new_x, new_y))
    return open_cells


def calculate_move_weight(projected: tuple[int, int], env: Environment, familiarity: int) -> float:
    """
    This is the numerator in equation 2 from the paper
    """
    projected_sf = env.static_field[projected[1]][projected[0]]
    # work around finite max float value
    if projected_sf >= float_info.max:
        return float_info.max
    return exp(familiarity * projected_sf)


def id_to_color(id_num: int) -> list[int]:
    r = random.Random(id_num)
    # Ensure that white and black (and values close) are not possible
    color_list = [r.randint(0, 180), r.randint(75, 255), r.randint(0, 255)]
    r.shuffle(color_list)
    return color_list


class PersonStrategy(Enum):
    COOPERATE = 1
    DEFECT = 2


class PersonGameState(Enum):
    NOT_PLAYED = 1
    WON = 2
    LOST = 3


class Person:
    def __init__(self, x: int, y: int, id_num: int, strategy: PersonStrategy, movement_strategy: MovementStrategy, strategy_inertia: float, update_interval: int, familiarity: int):
        self.x = x
        self.y = y
        self.id_num = id_num
        self.projected_x = 0
        self.projected_y = 0
        self.color = id_to_color(id_num)
        self.strategy = strategy
        self.movement_strategy = movement_strategy
        self.game_state = PersonGameState.NOT_PLAYED
        self.momentum = (0, 0)
        self.familiarity = familiarity
        self.strategy_inertia = strategy_inertia
        self.update_interval = update_interval

        self.history = []

    def findProjectedMove(self, env):
        self.game_state = PersonGameState.NOT_PLAYED
        if self.movement_strategy == MovementStrategy.RANDOM:
            self._findProjectedMoveRandom(env)
        elif self.movement_strategy == MovementStrategy.STATIC_FIELD or self.movement_strategy == MovementStrategy.STATIC_FIELD_WITH_MOMENTUM:
            self._findProjectedMoveStaticField(env)
        else:
            raise ValueError(f"Unknown movement strategy")

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
            cell, env, self.familiarity) for cell in open_cells]
        # If at exit ignore non-exits
        if max(move_weights) >= float_info.max:
            move_weights = [1.0 if weight >=
                            float_info.max else 0.0 for weight in move_weights]
        elif self.movement_strategy == MovementStrategy.STATIC_FIELD_WITH_MOMENTUM:
            for i, cell in enumerate(open_cells):
                dx = cell[0] - self.x
                dy = cell[1] - self.y

                momentum_weight = 3 - \
                    calculate_distance((dx, dy), self.momentum)
                move_weights[i] = move_weights[i] * exp(momentum_weight)

        total_weight = sum(move_weights)
        # The denominator in equation 2 from the paper
        probabilities = [weight / total_weight for weight in move_weights]
        move = random.choices(open_cells, weights=probabilities, k=1)[0]
        self.projected_x = move[0]
        self.projected_y = move[1]
        self.momentum = (self.projected_x - self.x,
                         self.projected_y - self.y)
        if self.movement_strategy == MovementStrategy.STATIC_FIELD_WITH_MOMENTUM:
            self.familiarity += 1

    # Function for person to choose what they will play in the prisoner's dilemma
    # True means cooperate, False means defect
    def playGame(self):
        if self.strategy == PersonStrategy.COOPERATE:
            return True
        elif self.strategy == PersonStrategy.DEFECT:
            return False
        else:
            raise ValueError("Unknown person strategy")

    def win(self, num_conflicts: int, num_cooperators: int):
        self.game_state = PersonGameState.WON if num_conflicts > 0 else PersonGameState.NOT_PLAYED
        self.history.append(
            [num_conflicts, num_cooperators, PersonGameState.WON])

    def lose(self, num_conflicts: int, num_cooperators: int):
        self.game_state = PersonGameState.LOST
        self.projected_x = self.x
        self.projected_y = self.y
        self.momentum = (0, 0)
        self.history.append(
            [num_conflicts, num_cooperators, PersonGameState.LOST])

    def update_strategy(self):
        if self.game_state == PersonGameState.NOT_PLAYED:
            self.history.append([0, 0, PersonGameState.NOT_PLAYED])

        self.game_state = PersonGameState.NOT_PLAYED
        if not self.history or (len(self.history) % self.update_interval) != 0:
            return

        # Calculate expected payoff for current strategy and the opposite strategy
        current_strat_payoff = 0.0
        opposite_strat_payoff = 0.0
        num_conflicts = sum(record[0] for record in self.history)
        num_cooperators = sum(record[1] for record in self.history)

        if num_conflicts == 0:
            return  # No conflicts, no strategy update

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
                opposite_strat_payoff = 1 / \
                    ((num_conflicts - num_cooperators) ** 2)
            if self.strategy == PersonStrategy.DEFECT:
                current_strat_payoff = 1 / \
                    ((num_conflicts - num_cooperators) ** 2)
                opposite_strat_payoff = 0.0
        # Calculate probability of changing strategy
        current_strat_payoff = self.strategy_inertia * current_strat_payoff
        probability = 1 / \
            (1 + exp((current_strat_payoff - opposite_strat_payoff)/0.1))
        # Change strat based on probability
        if random.random() <= probability:
            if self.strategy == PersonStrategy.COOPERATE:
                self.strategy = PersonStrategy.DEFECT
            elif self.strategy == PersonStrategy.DEFECT:
                self.strategy = PersonStrategy.COOPERATE

        self.history = []

    def __str__(self):
        return f"Person(id={self.id_num}, x={self.x}, y={self.y}, s={self.strategy})"
