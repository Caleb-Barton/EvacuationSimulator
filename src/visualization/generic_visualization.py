from abc import ABC, abstractmethod


class StepData:
    def __init__(self, grid_state: list[list[str | object]], escaped_people: list[int]):
        self.grid_state = [row.copy() for row in grid_state]
        self.escaped_people = escaped_people.copy()


class GenericVisualization(ABC):

    def __init__(self):
        self.history: list[StepData] = []

    def record_step(self, step_data: StepData):
        self.history.append(step_data)

    @abstractmethod
    def export(self, verbose):
        """
        Abstract method to create a plot or animation of the evacuation process.
        Must be implemented by subclasses.
        """
        pass
