import dataclasses

@dataclasses.dataclass
class State_DataClass:
    distance: tuple
    position: tuple
    relative_state: str
    food: tuple