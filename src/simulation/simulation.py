import copy
import random
from environment import Environment
from person import Person, MovementStrategy, PersonStrategy, PersonGameState
from visualization import GenericVisualization, StepData


def prisoners_dilemma(person_list: list[Person], location: tuple[int, int], verbose=False):
    """
    Function to play the prisoner's dilemma game when there is a conflict
    among multiple people trying to move to the same cell.

    Assumed P=2 for simplicity.
    """

    if len(person_list) < 2:
        raise ValueError(
            "prisoner dilemma was called with less than 2 people")

    actions: list[bool] = []
    collaborator_list: list[Person] = []
    defector_list: list[Person] = []
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
        winner.win(num_conflicts=len(person_list),
                   num_cooperators=len(collaborator_list))
    elif len(defector_list) == 1:
        # Lone defector wins
        winner = defector_list[0]
        defector_list[0].win(num_conflicts=len(person_list),
                             num_cooperators=len(collaborator_list))
    else:
        # competition between all defectors
        if random.random() < 1/len(defector_list):
            winner = random.choice(defector_list)
            winner.win(num_conflicts=len(person_list),
                       num_cooperators=len(collaborator_list))
    [person.lose(len(person_list), len(collaborator_list))
     for person in collaborator_list if person != winner]
    [person.lose(len(person_list), len(collaborator_list))
     for person in defector_list if person != winner]
    if verbose:
        print(
            f"Prisoner's Dilemma at {location}:\n\tcooperate: {[str(c) for c in collaborator_list]}\n\tdefect: {[str(d) for d in defector_list]}\n\tWinner: {winner}")


def spawn_people(env, cooperate_percent: float, inertia: float,
                 update_interval: int, strategy_inertia: float,
                 movement_strategy=MovementStrategy.STATIC_FIELD, spawn_percent=1.0):
    """
    Function to spawn people in the environment at random spawn points.
    """
    spawn_count = int(len(env.spawn_points) * spawn_percent)
    selected_spawns = random.sample(env.spawn_points, spawn_count)
    count = 0
    for x, y in selected_spawns:
        count += 1
        person_char = count
        if random.random() < cooperate_percent:
            strategy = PersonStrategy.COOPERATE
        else:
            strategy = PersonStrategy.DEFECT
        env.grid[y][x] = Person(x=x, y=y, id_num=person_char,
                                movement_strategy=movement_strategy, strategy=strategy, inertia=inertia, strategy_inertia=strategy_inertia,
                                update_interval=update_interval)


def move(env):
    """
    Function to move each person in the environment to their projected position.
    """

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
                    env_copy.escaped_people.append(current_person.id_num)
    return env_copy


def update_strategy(env):
    for row in range(len(env.grid)):
        for col in range(len(env.grid[row])):
            current_value = env.grid[row][col]
            if isinstance(current_value, Person):
                current_person = current_value
                current_person.update_strategy()


def identify_move_conflicts(env, x, y):
    """
    Function to identify if multiple people are trying to move to the same cell.
    Returns a list of people trying to move to the cell at (x, y)."""

    if not env.is_walkable(x, y):
        return []
    conflict_people = []
    people_nearby = env.get_people_nearby(x, y)
    for person in people_nearby:
        if person.projected_x == x and person.projected_y == y:
            conflict_people.append(person)
    return conflict_people


def game_loop(env: Environment, visualizers: list[GenericVisualization], verbose: bool):
    """
    Function to loop through the grid moving people while there are still those who haven't reached the exit
    """
    iteration = 0
    while any(isinstance(item, Person) for row in env.grid for item in row):
        if verbose:
            print(f"Iteration {iteration}:")
        # Find projected moves for each player
        for row in env.grid:
            for item in row:
                if isinstance(item, Person):
                    item.findProjectedMove(env)
        # Play the prisoner's dilemma if any two people have the same projected moves
        for y in range(len(env.grid)):
            for x in range(len(env.grid[y])):
                person = env.grid[y][x]
                conflict_people = identify_move_conflicts(env, x, y)
                if len(conflict_people) > 1:
                    prisoners_dilemma(
                        conflict_people, location=(x, y), verbose=verbose)
                elif isinstance(person, Person):
                    person.win(num_conflicts=0, num_cooperators=0)
        # Move each player
        env = move(env)
        [visualizer.record_step(
            StepData(
                grid_state=env.grid,
                escaped_people=env.escaped_people
            )) for visualizer in visualizers]
        if verbose:
            print(f"Updating strategies...")
        update_strategy(env)
        iteration += 1
        if verbose:
            print()
    if verbose:
        print(f"All people have evacuated in {iteration} iterations.")
        print(
            f"Escaped people: {[id_num for id_num in env.escaped_people]}")

    [visualizer.export(verbose) for visualizer in visualizers]


def run_simulation(movement_strategy: MovementStrategy, env: Environment, visualizers: list[GenericVisualization], spawn_percent: float, cooperate_percent: float, inertia: float, update_interval: int, strategy_inertia: float, verbose=True):
    """
    Primary entry point to run the evacuation simulation.
    Outputs data via the provided visualizers.
    """

    spawn_people(env, movement_strategy=movement_strategy,
                 spawn_percent=spawn_percent, cooperate_percent=cooperate_percent, inertia=inertia, strategy_inertia=strategy_inertia, update_interval=update_interval)
    [visualizer.record_step(
        StepData(
            grid_state=env.grid,
            escaped_people=env.escaped_people
        )) for visualizer in visualizers]
    game_loop(env=env, visualizers=visualizers,
              verbose=verbose)
