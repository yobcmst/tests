import abc
import pandas as pd

class DocumentCollection:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.csv_df = pd.read_csv(csv_path)
        self.add_csv_df()
        self.items = dict()

    def _add_item(self, row: pd.Series):
        item_id = row['item_id']
        text = row['text']
        if item_id not in self.items:
            self.items[item_id] = BaseItem(item_id, text)
        self.items[item_id].add_mention(row, item_id)

    def add_csv_df(self):
        for idx, row in self.csv_df.iterrows():
            self._add_item(row)

class BaseItem:
    num_max_ment: int=10
    def __init__(self, item_id: str, text: str):
        self.item_id = item_id
        self.text = text
        self.ments = {}

    def _get_item_ids(self):
        m_ids = list(self.ments.keys())
        item_ids = [m_id.split("_m")[0] for m_id in m_ids]
        return list(set(item_ids))

    def _get_max_ment_id(self, item_id: str):
        m_ids = list(self.ments.keys())
        max_ment_id = max(
            [
                m_id.split("_m")[1] 
                for m_id in m_ids
                if m_id.split("_m")[0] == item_id
            ]
        )

    def add_mention(self, row: pd.Series, item_id: str):
        """
            ment_id format:
                f"{item_id}_m1", f"{item_id}_m2", f"{item_id}_m3" ... etc
        """
        cur_item_ids = self._get_item_ids()
        if item_id not in cur_item_ids:
            ment_id = f"{item_id}_m1"
        else:
            max_ment_id = self._get_max_ment_id(item_id)
            ment_id = f"{item_id}_m{max_ment_id+1}"
        ment_text = row['mention_text']
        if ment_id not in self.ments:
            self.ments[ment_id] = MentionICD(ment_id, ment_text)
        self.ments[item_id].add_codes(row)

class BaseMention(metaclass=abc.ABCMeta):
    def __init__(self, ment_id: str, ment_text: str):
        self.ment_id = ment_id
        self.ment_text = ment_text
        self.codes = dict()    

    @abc.abstractmethod
    def add_codes(self, row: pd.Series):
        ...


class MentionICD(BaseMention):
    num_max_codes: int=4
    def __init__(self, ment_id: str, ment_text: str):
        super().__init__(ment_id, ment_text)

    def add_codes(self, row: pd.Series):
        for c_idx in range(1, self.num_max_codes+1):
            code = row[f"ICDCode_{c_idx}"]
            cn = row[f"中文名稱_{c_idx}"]
            if code not in self.codes:
                self.codes[code] = ICDCode(code, cn)

class MentionOccupat(BaseMention):
    def __init__(self, ment_id: str, ment_text: str):
        super().__init__(ment_id, ment_text)
        self.code_column = ""
        self.cn_column = ""

    def add_codes(self, row: pd.Series):
        code = row[f"{code_column}"]
        cn = row[f"{cn_column}"]
        if code not in self.codes:
            self.codes[code] = OccupatCode(code, cn)

class BaseCode:
    def __init__(self, code: str, cn: str):
        self.code = code
        self.cn = cn

class ICDCode(BaseCode):
    pass

class OccupatCode(BaseCode):
    pass
