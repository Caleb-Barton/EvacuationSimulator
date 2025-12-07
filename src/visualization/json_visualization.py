from .generic_visualization import GenericVisualization, StepData
import json
from person import Person, PersonStrategy
from person.person import MovementStrategy
import os


class JsonVisualization(GenericVisualization):
    def __init__(self, filename: str, environment_name: str, strategy: MovementStrategy):
        super().__init__()
        self.filename = filename
        self.environment_name = environment_name
        self.strategy = strategy.name
        self.strategy_distribution = []
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

    def record_step(self, step_data: StepData):
        super().record_step(step_data)
        num_people = 0
        strategy_count = {strategy: 0 for strategy in PersonStrategy}
        for row in step_data.grid_state:
            for item in row:
                if isinstance(item, Person):
                    num_people += 1
                    strategy_count[item.strategy] += 1
        for person in step_data.escaped_people:  # type: ignore
            person: Person = person
            num_people += 1
            strategy_count[person.strategy] += 1
        if num_people > 0:
            distribution = {strategy.name: count /
                            num_people for strategy, count in strategy_count.items()}
        else:
            distribution = {strategy.name: 0.0 for strategy in PersonStrategy}
        self.strategy_distribution.append(distribution)

    def export(self, verbose):
        with open(self.filename, 'w') as f:
            json.dump({
                "environment": self.environment_name,
                "people_count": self.get_people_count(),
                "strategy": self.strategy,
                'escape_time_history': self.get_escape_time_history(),
                'strategy_distribution': self.strategy_distribution
            }, f, indent=4)
        if verbose:
            print("Saved evacuation data to " + self.filename)

    def get_escape_time_history(self) -> list[int]:
        return [len(h.escaped_people) for h in self.history]

    def get_people_count(self) -> int:
        if not self.history:
            return 0
        initial_step = self.history[0]
        count = 0
        for row in initial_step.grid_state:
            for item in row:
                if isinstance(item, Person):
                    count += 1
        return count
