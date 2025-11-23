import copy
import random
from environment import Environment
from person import Person, MovementStrategy
import sys
from visualization import GenericVisualization, StepData, VideoVisualization, JsonVisualization


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
    char_pool = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    if spawn_count > len(char_pool):
        raise ValueError("Not enough unique characters to represent people")
    for x, y in selected_spawns:
        person_char = char_pool.pop(0)
        env.grid[y][x] = Person(x, y, person_char, strategy)


# Function to actually move each person once their desired move is chosen
def move(env):
    env_copy = copy.deepcopy(env)
    # Loop through each item in the environment and look for people
    for row in range(len(env.grid)):
        for col in range(len(env.grid[row])):
            current_value = env.grid[row][col]
            if isinstance(current_value, Person):
                current_person = current_value
                # Remove the current person from their current position
                env_copy.grid[row][col] = " "
                # Change the current person's x and y values to where they wanted to move
                current_person.x = current_person.projected_x
                current_person.y = current_person.projected_y
                # If they are not moving to an exit, move them in the environment
                if not (env.grid[current_person.y][current_person.x] == "E"):
                    env_copy.grid[current_person.y][current_person.x] = current_person
                else:
                    env_copy.escaped_people.append(current_person.letter)
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


def game_loop(env: Environment, visualizers: list[GenericVisualization]):
    """
    Function to loop through the grid moving people while there are still those who haven't reached the exit
    """
    iteration = 0
    while any(isinstance(item, Person) for row in env.grid for item in row):
        # Find projected moves for each player
        for row in env.grid:
            for item in row:
                if isinstance(item, Person):
                    item.findProjectedMove(env)
        # Play the prisoner's dilemma if any two people have the same projected moves
        for y in range(len(env.grid)):
            for x in range(len(env.grid[y])):
                conflict_people = identify_move_conflicts(env, x, y)
                if len(conflict_people) > 1:
                    prisoners_dilemma(conflict_people)
        # Move each player
        env = move(env)
        print(env)
        [visualizer.record_step(
            StepData(
                grid_state=env.grid,
                escaped_people=env.escaped_people
            )) for visualizer in visualizers]
        iteration += 1
    print(f"All people have evacuated in {iteration} iterations.")
    print(
        f"Escaped people: {[letter for letter in env.escaped_people]}")

    [visualizer.export() for visualizer in visualizers]


def find_argument_value(arg_name: str, default: str) -> str:
    args = [arg for arg in sys.argv if arg.startswith(f"--{arg_name}=")]
    if args:
        return args[0].split("=")[1]
    return default


def find_strategy_argument() -> MovementStrategy:
    strategy_name = find_argument_value("strategy", "static")
    if not strategy_name:
        return MovementStrategy.STATIC_FIELD
    strategy_name = strategy_name.lower()
    if strategy_name == "random":
        return MovementStrategy.RANDOM
    else:
        return MovementStrategy.STATIC_FIELD


def main():
    strategy = find_strategy_argument()
    env_name = find_argument_value("env", "env1")
    env = Environment(env_name)

    json_filename = find_argument_value("json", "")
    video_filename = find_argument_value("video", "")
    visualizers: list[GenericVisualization] = []
    if video_filename:
        fps_str = find_argument_value("fps", "2")
        fps = int(fps_str) if fps_str else 2
        visualizers.append(VideoVisualization(
            filename=video_filename,
            fps=fps
        ))
    if json_filename:
        visualizers.append(JsonVisualization(
            filename=json_filename,
            environment_name=env_name,
            strategy=strategy))

    spawn_people(env, strategy, spawn_percent=0.75)
    print(env)
    game_loop(env=env, visualizers=visualizers)


if __name__ == "__main__":
    main()
