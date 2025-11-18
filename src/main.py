import copy
import random
from environment import Environment
from person import Person, MovementStrategy
import sys


def get_rand_char():
    return chr(int(random.random() * 26) + ord('a'))

# Function to play the prisoner's dilemma game when there is a conflict
# We've assumed P = 2 (it was mathematically the easiest to implement )
def prisoners_dilemma(person_list):
    if len(person_list) < 2:
        raise ValueError(
            "prisoner dilemma was called with less than 2 people")
    actions = []
    collaborator_list = []
    defector_list = []
    for person in person_list:
        actions.append(person.playGame())
    for index, person in enumerate(person_list):
        if actions[index]:
            collaborator_list.append(person)
        else:
            defector_list.append(person)
    winner = None
    if len(defector_list) == 0:
        # All collaborate! Choose a random collaborator to win
        winner = random.choice(collaborator_list)
        winner.win()
    elif len(defector_list) == 1:
        # Lone defector wins
        winner = defector_list[0]
        defector_list[0].win()
    else:
        # competition between all defectors
        winner = random.choice(defector_list)
        if random.random() < 1/len(defector_list):
            winner.win()
        else:
            winner.lose()
    [person.lose() for person in collaborator_list if person != winner]
    [person.lose() for person in defector_list if person != winner]

# Replace spawn points with people objects
def spawn_people(env, strategy=MovementStrategy.STATIC_FIELD, spawn_percent=1.0):
    spawn_count = int(len(env.spawn_points) * spawn_percent)
    selected_spawns = random.sample(env.spawn_points, spawn_count)
    for x, y in selected_spawns:
        env.grid[y][x] = Person(x, y, get_rand_char(), strategy)


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
                else:
                    env_copy.escaped_people.append(current_person)
    return env_copy

def identify_move_conflicts(env, x, y):
    if not env.is_walkable(x, y):
        return []
    conflict_people = []
    people_nearby = env.get_people_nearby(x, y)
    for person in people_nearby:
        if person.projected_x == x and person.projected_y == y:
            conflict_people.append(person)
    return conflict_people

# Function to loop through the grid moving people while there are still those who haven't reached the exit
def game_loop(env):
    iteration = 0
    while any(isinstance(item, Person) for row in env.grid for item in row):
        # Find projected moves for each player
        for row in env.grid:
            for item in row:
                if isinstance(item, Person):
                    item.findProjectedMove(env)
        # Play the prisoner's dilemma if any two people have the same projected moves
        for y in range(len(env.grid)):
            for x in range(len(row)):
                conflict_people = identify_move_conflicts(env, x, y)
                if len(conflict_people) > 1:
                    prisoners_dilemma(conflict_people)
        # Move each player
        env = move(env)
        print(env)
        iteration += 1
    print(f"All people have evacuated in {iteration} iterations.")
    print(f"Escaped people: ", end="")
    for person in env.escaped_people:
        print(f"{person.letter}", end=", ")


def main():
    if "--strategy=random" in sys.argv:
        strategy = MovementStrategy.RANDOM
    else:
        strategy = MovementStrategy.STATIC_FIELD

    env1 = Environment("env1")
    spawn_people(env1, strategy, spawn_percent=0.75)

    # print initial environment 
    print(env1)

    game_loop(env1)


if __name__ == "__main__":
    main()
