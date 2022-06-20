import abc
from typing import List, Dict, Union

from .code import BaseCode, ICDCode, OccupatCode

class BaseMention(abc.ABC):
    def __init__(self, ment_id: str, ment_text: str, codes: Union[None, BaseCode, Dict[str, BaseCode], List[BaseCode]]=None):
        self.ment_id = ment_id
        self.ment_text = ment_text
        if codes is not None:
            if isinstance(codes, BaseCode):
                codes = {codes.code: codes}
            elif isinstance(codes, list):
                for c in codes:
                    assert isinstance(c, BaseCode)
                codes = {c.code: c for c in codes}
            elif isinstance(codes, dict):
                for c, v in codes.items():
                    assert isinstance(c, str)
                    assert isinstance(v, BaseCode)
        self.codes: Dict[str, BaseCode] = codes

    def get_ment_id(self):
        return self.ment_id

    def get_ment_text(self):
        return self.ment_text

    def add_code(self, code: BaseCode):
        assert isinstance(code, BaseCode)
        self.codes[code.code] = code

    def add_codes(self, codes: List[BaseCode]):
        for c in codes:
            assert isinstance(c, BaseCode)
            self.add_code(c)

    def __repr__(self):
        repr_str =  f"{self.__class__.__name__}("
        repr_str += ")"
        return repr_str


class MentionICD(BaseMention):
    def get_mention_text(self):
        ...

class MentionOccupat(BaseMention):
    def get_code(self):
        ...

class MentionFactory(abc.ABC):
    @abc.abstractmethod
    def createMention(self) -> BaseMention:
        ...

class MentionICDFactory(MentionFactory):
    def createMention(self):
        return MentionICD()

class MentionOccupatFactory(MentionFactory):
    def createMention(self):
        return MentionOccupat()