import enum
import pandas as pd
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Union, Optional, Tuple

@dataclass
class BaseCode:
    code: str
    value: str

@dataclass
class ICD10CMCode(BaseCode):
    pass

@dataclass
class ICD10PCSCode(BaseCode):
    pass

@dataclass
class OccupatCode(BaseCode):
    pass

@dataclass
class MentionText:
    text: str
    span: Tuple[int, int]
    context_left: str
    context_right: str

@dataclass
class MentionInfo:
    mention: MentionText
    label: List[Union[BaseCode, ICD10CMCode, ICD10PCSCode]]

@dataclass
class DocInfo:
    id: str
    text: str
    mention_info_lst: Optional[List[MentionInfo]]
    def add_mention(self, mention_info: MentionInfo):
        assert isinstance(mention_info, MentionInfo)
        self.mention_info_lst.append(mention_info)

    def __add__(self, other: DocInfo):
        assert isinstance(other, DocInfo)
        assert self.id == other.id
        assert self.text == other.text
        cur_mention_text_lst: List[str] = [
            m_info.mention.text for m_info in self.mention_info_lst
        ]
        for m_info in other.mention_info_lst:
            if m_info.mention.text not in cur_mention_text_lst:
                self.add_mention(m_info)

@dataclass
class DocDataset:
    name: name
    docs: List[DocInfo]

class MentionFileIO:
    def __int__(self, path: str):
        self.path = path

    def read(self) -> pd.DataFrame:
        pass


def split_diagnosis_and_remarks_from_text(text: str):
    tag = {"diagnosis": "@diagnosis@",
           "remarks": "@remarks@"}
    text_new = ""
    for t in text.split("\n"):
        if (tag["diagnosis"] in t):
            text_new += "\n"+t
        elif (tag["remarks"] in t):
            text_new += t
        elif t == "":
            pass
        else:
            text_new += t+"\n"
    text_split = text_new.split("\n")
    assert len(text_split) == 4
    diagnosis_text = text_split[1].replace(tag["diagnosis"], "")
    remarks_text = text_split[2].replace(tag["remarks"], "")
    return {"diagnosis": diagnosis_text, "remarks": remarks_text}

def is_diagnosis_or_precedure_code(code: str):
    if (len(code) == 3) and ("." not in code):
        return "diagnosis"
    elif "." not in code:
        return "precedure"
    elif "." in code:
        return "diagnosis"
    else:
        return "None"

class CodeEnum(str, enum.Enum):
    diagnosis: "diagnosis"
    precedure: "precedure"
    occupat: "occupat"

class MentionPreprocessor:
    def __init__(self):
        self.docs: Dict[str, DocInfo] = {}

    def _is_has_diagnosis_and_remark(self, text: str):
        return True if "@diagnosis@" in text and "@remarks@" in text else False

    def process(self, df: pd.DataFrame):
        for idx, row in df.iterrows():
            res = self.process_one_row(row)

    def process_one_row(self, row: pd.Series):
        doc_id = row['doc_id']
        text = self.process_text(row['text'])
        mention = self.process_mention_text(row['mention_text'], text)
        label = self.process_code(row['label'])
        mention_info = MentionInfo(mention, label)
        if doc_id not in self.docs:
            mention_info_lst = [mention_info]
            doc_info = DocInfo(id=doc_id, text=text, mention_info_lst=mention_info_lst)
            self.docs[doc_id] = doc_info
        else:
            self.doc[doc_id].add_mention(mention_info)

    def process_code(self, code_info: Union[List[Tuple[str, str]], Tuple[str, str]]):
        """
            code_info: 
                [("A01", "霍亂"), ("XX", "Descr_XXXX")]
            or ("A01", "霍亂")
        """
        code_info_res = []
        if isinstance(code_info, tuple):
            code_info = [code_info]
        for c_info in code_info:
            assert isinstance(c_info, tuple)
            code, value = c_info
            assert isinstance(code, str)
            assert isinstance(value, str)
            c_info_res = self.process_one_code(code, value)
            code_info_res.append(c_info_res)
        return code_info_res
    
    def process_one_code(self, code: str, value: str):
        code_type = is_diagnosis_or_precedure_code(code)
        if code_type == CodeEnum.diagnosis:
            return ICD10CMCode(code, value)
        elif code_type == CodeEnum.precedure:
            return ICD10PCSCode(code, value)
        elif code_type == CodeEnum.occupat:
            return OccupatCode(code, value)

    def process_text(self, text: str):
        if self._is_has_diagnosis_and_remark(text):
            split_res = split_diagnosis_and_remarks_from_text(text)
            diag, remarks = split_res['diagnosis'], split_res['remarks']
            text = " ".join([diag, remarks])
        return text

    def process_mention_text(self, mention_text: str, text: str):
        mention_span = self.get_mention_span(mention_text, text)
        mention_context = self.get_mention_context(mention_text, text)
        mention = MentionText(mention_text, mention_span, mention_context['left'], mention_context['right'])
        return mention

    def get_mention_span(self, mention_text: str, text: str) -> Tuple[int, int]:
        # TODO TODO TODO
        mention_span = (0, 1)
        return mention_span

    def get_mention_context(self, mention_text: str, text: str) -> Dict[str, str]:
        # TODO TODO TODO
        mention_context = {"left": "", "right": ""}
        return mention_context

