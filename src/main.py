import copy
import random
from environment import Environment
from person import Person, MovementStrategy
import sys


# Function to play the prisoner's dilemma game when there is a conflict
def prisonersDilemma(person1, person2):
    advancing_player = None
    # Right now this only checks if both people cooperate and chooses a random one between the two
    # Add the other prisoner's dilemma options later
    if person1.playGame() == "C" and person2.playGame() == "C":
        advancing_player = random.randint(1, 2)
    # If Player 1 gets to advance, remove Player 2's projected move so they stay still
    if advancing_player == 1:
        person2.projected_x = person2.x
        person2.projected_y = person2.y
    # If Player 2 gets to advance, remove Player 1's projected move so they stay still
    else:
        person1.projected_x = person1.x
        person1.projected_y = person1.y


# Function to actually move each person once their desired move is chosen
def move(env):
    env_copy = copy.deepcopy(env)
    # Loop through each item in the environment and look for people
    for row in range(len(env.grid)):
        for col in range(len(env.grid[row])):
            if type(env.grid[row][col]) is Person:
                current_person = env.grid[row][col]
                # Remove the current person from their current position
                env_copy.grid[row][col] = " "
                # Change the current person's x and y values to where they wanted to move
                current_person.x = current_person.projected_x
                current_person.y = current_person.projected_y
                # If they are not moving to an exit, move them in the environment
                if not (env.grid[current_person.y][current_person.x] == "E"):
                    env_copy.grid[current_person.y][current_person.x] = current_person
    return env_copy


# Function to loop through the grid moving people while there are still those who haven't reached the exit
def gameLoop(env):
    iteration = 0
    while any(isinstance(item, Person) for row in env.grid for item in row):
        # Find projected moves for each player
        for row in env.grid:
            for item in row:
                if isinstance(item, Person):
                    item.findProjectedMove(env)
        # Play the prisoner's dilemma if any two people have the same projected moves
        for row in env.grid:
            for item in row:
                if isinstance(item, Person):
                    for row2 in env.grid:
                        for item2 in row2:
                            if isinstance(item2, Person):
                                if item.projected_x == item2.projected_x and item.projected_y == item2.projected_y and item != item2:
                                    prisonersDilemma(item, item2)
        # Move each player
        env = move(env)
        print(env)
        iteration += 1
    print(f"All people have evacuated in {iteration} iterations.")


def main():
    if "--strategy=random" in sys.argv:
        strategy = MovementStrategy.RANDOM
    else:
        strategy = MovementStrategy.STATIC_FIELD

    # This kickoff only works for env1
    # We should change the whole thing later but for now you can visualize each person as their own letter
    alphabet = ["A", "B", "C", "D", "E", "F"]
    count = 0
    env1 = Environment("env1")
    for row in range(len(env1.grid)):
        for col in range(len(env1.grid[row])):
            if env1.grid[row][col] == "S":
                env1.grid[row][col] = Person(
                    col, row, alphabet[count], strategy=strategy)
                count += 1
    # print initial environment
    print(env1)

    gameLoop(env1)


if __name__ == "__main__":
    main()
