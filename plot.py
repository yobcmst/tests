import abc
from abc import abstractmethod

import pandas as pd

class PlotInterface(abc.ABC):
    @abstractmethod
    def plot(self, df: pd.DataFrame):
        ...

class BasePlot(PlotInterface):
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def __repr__(self):
        name = self.__class__.__name__
        values = tuple(self.__dict__.values())
        return f'({name}): {values}'        

class PlotPie(BasePlot):
    def __init__(self, df):
        super(PlotPie, self).__init__(df)

    def plot(self, df: pd.DataFrame):
        pass


class PlotHistogram(BasePlot):
    def __init__(self, df):
        super(PlotHistogram, self).__init__(df)

    def plot(self, df: pd.DataFrame):
        pass    

def plot(elements: List[BasePlot]):
    for e in elements:
        e.plot()


if __name__ == "__main__":
    data_pie = pd.DataFrame({"a": 1})
    data_hist = pd.DataFrame({"a": 1})
    
    plot([
        PlotPie(data_pie),
        PlotHistogram(data_hist),
    ])
