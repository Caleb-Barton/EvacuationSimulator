import random


class Person:
    def __init__(self, x, y, letter):
        self.x = x
        self.y = y
        self.letter = letter
        self.projected_x = 0
        self.projected_y = 0

    # Function for person to decide where they want to move next
    def findProjectedMove(self, env):
        # Right now people choose a random empty square (up, down, left, right) they want to move to
        # Change this in the future to have them want to move based on an algorithm
        possible_move_list = []
        if env.is_walkable(self.x + 1, self.y):
            possible_move_list.append((self.x + 1, self.y))
        if env.is_walkable(self.x - 1, self.y):
            possible_move_list.append((self.x - 1, self.y))
        if env.is_walkable(self.x, self.y + 1):
            possible_move_list.append((self.x, self.y + 1))
        if env.is_walkable(self.x, self.y - 1):
            possible_move_list.append((self.x, self.y - 1))
        # If they can't move anywhere, stay still
        if len(possible_move_list) == 0:
            possible_move_list.append((self.x, self.y))
        move_idx = random.randint(0, len(possible_move_list) - 1)
        move = possible_move_list[move_idx]
        self.projected_x = move[0]
        self.projected_y = move[1]

    # Function for person to choose what they will play in the prisoner's dilemma
    def playGame(self):
        # Right now the players only ever return "C" for cooperate
        # Change this in the future to have them choose different options
        return "C"

    def __str__(self):
        return self.letter
