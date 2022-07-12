from dataclasses import dataclass
from dacite import from_dict
from typing import Optional, List, Union


@dataclass
class FunctionSvals:
    Rate: List[int]  # Exception: 83 Solomon
    Turn: Optional[List[int]]
    Count: Optional[List[int]]
    Value: Optional[List[int]]
    Value2: Optional[List[int]]


@dataclass
class SkillFunction:
    type: str
    target_type: str
    target_team: str
    name: str
    icon: Optional[str]
    buff_type: Optional[str]
    svals: Union[FunctionSvals, List[dict]]

    def __post_init__(self):
        sval_dict = {key: [i[key] for i in self.svals] for key in self.svals[0]}
        self.svals = from_dict(data_class=FunctionSvals, data=sval_dict)
