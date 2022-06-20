import abc

class BaseCode(abc.ABC):
    @abc.abstractmethod
    def get_code(self):
        ...

class ICDCode(BaseCode):
    def get_code(self):
        ...

class OccupatCode(BaseCode):
    def get_code(self):
        ...

class CodeFactory(abc.ABC):
    @abc.abstractmethod
    def createCode(self) -> BaseCode:
        ...

class ICDCodeFactory(CodeFactory):
    def createCode(self):
        return ICDCode()

class OccupatCodeFactory(CodeFactory):
    def createCode(self):
        return OccupatCode()