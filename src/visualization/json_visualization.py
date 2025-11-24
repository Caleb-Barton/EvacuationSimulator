from .generic_visualization import GenericVisualization, StepData
import json
from person import Person
from person.person import MovementStrategy
import os


class JsonVisualization(GenericVisualization):
    def __init__(self, filename: str, environment_name: str, strategy: MovementStrategy):
        super().__init__()
        self.filename = filename
        self.environment_name = environment_name
        self.strategy = strategy.name
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

    def export(self):
        with open(self.filename, 'w') as f:
            json.dump({
                "environment": self.environment_name,
                "people_count": self.get_people_count(),
                "strategy": self.strategy,
                'escape_time_history': self.get_escape_time_history()
            }, f, indent=4)

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
