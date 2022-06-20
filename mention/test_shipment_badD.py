from typing import List
from dataclasses import dataclass

class Shipment:
    def __init__(self):
        self.boxes: List[Box] = []

    def getWeight(self):
        w = 0
        for b in self.boxes:
            for item in b.getItems():
                w += item.weight
        return w

class Box:
    def __init__(self):
        self._items: List[item] = []

    def getItems(self) -> List[item]:
        return self._items

@dataclass
class Item:
    containedIn: Box
    weight: int