class DeprecatedBaseItem:
    def __init__(self, item_id: str, text: str, ments: Union[None, BaseMention, List[BaseMention], Dict[str, BaseMention]]):
        self.item_id = item_id
        self.text = text
        if ments is not None:
            if isinstance(ments, BaseMention):
                ments = {ments.ment_id: ments}
            elif isinstance(ments, list):
                for m in ments:
                    assert isinstance(m, BaseMention)
                ments = {m.ment_id: m for m in ments}
            elif isinstance(ments, dict):
                for m_id, m in ments.items():
                    assert isinstance(m_id, str)
                    assert isinstance(m, BaseMention)
        self.ments: Dict[str, BaseMention] = ments

    def add_ment(self, m: BaseMention):
        assert isinstance(m, BaseMention)
        if m.ment_id not in self.ments:
            self.ments[m.ment_id] = m