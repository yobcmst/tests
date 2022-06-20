from dataclasses import dataclass
from random import randint

class ToDict:
    def to_dict(self):
        data = {
            k: v for k, v in vars(self).items() 
            if not k.startswith('_')
        }
        return data  

class ToJson(ToDict):
    def to_json(self):
        import json
        return json.dumps(super().to_dict())

class ToPickle(ToDict):
    def to_pickle(self):
        import pickle
        return pickle.dumps(super().to_dict())

class Serialize(ToJson, ToPickle, ToDict):
    pass


@dataclass
class hasHealth:
    HEALTH_MIN: int = 10
    HEALTH_MAX: int = 20
    _health: int = 0  
    def __post_init__(self) -> None:
        self._health = randint(self.HEALTH_MIN, self.HEALTH_MAX)

    def is_alive(self) -> bool:
        return self._health > 0

    def is_dead(self) -> bool:
        return self._health <= 0

@dataclass
class hasPosition:
    _position_x: int = 0
    _position_y: int = 0
    def position_set(self, x: int, y: int) -> None:
        self._position_x = x
        self._position_y = y

    def position_change(self, right=0, left=0, down=0, up=0):
        x = self._position_x + right - left
        y = self._position_y + down - up
        self.position_set(x, y)

    def position_get(self) -> tuple:
        return self._position_x, self._position_y    


class Hero_1(hasHealth, hasPosition, Serialize):
    pass

class Hero_2(hasPosition, hasHealth, Serialize):
    pass


@dataclass
class HeroOld:
    HEALTH_MIN: int = 10
    HEALTH_MAX: int = 20
    _health: int = 0
    _position_x: int = 0
    _position_y: int = 0

    def position_set(self, x: int, y: int) -> None:
        self._position_x = x
        self._position_y = y

    def position_change(self, right=0, left=0, down=0, up=0):
        x = self._position_x + right - left
        y = self._position_y + down - up
        self.position_set(x, y)

    def position_get(self) -> tuple:
        return self._position_x, self._position_y

    def __post_init__(self) -> None:
        self._health = randint(self.HEALTH_MIN, self.HEALTH_MAX)

    def is_alive(self) -> bool:
        return self._health > 0

    def is_dead(self) -> bool:
        return self._health <= 0



class IrisInterface:
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    species: str

    def __init__(self,
                 sepal_length: float,
                 sepal_width: float,
                 petal_length: float,
                 petal_width: float,
                 species: str) -> None:
        raise NotImplementedError

    def mean(self) -> float:
        raise NotImplementedError

    def sum(self) -> float:
        raise NotImplementedError

    def len(self) -> int:
        raise NotImplementedError


class Setosa(IrisInterface):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    species: str

    def __init__(self,
                 sepal_length: float,
                 sepal_width: float,
                 petal_length: float,
                 petal_width: float,
                 species: str) -> None:
        self.sepal_length = sepal_length
        self.sepal_width = sepal_width
        self.petal_length = petal_length
        self.petal_width = petal_width
        self.species = species

    def _get_values(self):
        return [x for x in vars(self).values()
                  if isinstance(x, (float,int))]

    def mean(self) -> float:
        return self.sum() / self.len()

    def sum(self) -> float:
        return sum(self._get_values())

    def len(self) -> int:
        return len(self._get_values())

from IPython import embed; embed()
