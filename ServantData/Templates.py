from dataclasses import dataclass
from dacite import from_dict
from typing import Optional, List, Union, Dict


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


@dataclass
class ServantInput:
    id: int
    collection_no: int
    name: str
    class_name: str
    rarity: int
    cost: int
    attribute: str
    star_absorb: int
    star_gen: int
    death_chance: int
    cards: List[str]
    hit_distribution: Dict
    atk_base: int
    atk_max: int
    hp_base: int
    hp_max: int
    atk_growth: List[int]
    hp_growth: List[int]
    bond: List[int]
    exp: List[int]


@dataclass
class Buff:
    description: str
    level: Union[List[int], List[str]]
    icon: str


@dataclass
class Skill:
    name: str
    detail: str
    icon: str
    num: int
    priority: int
    cooldown: List[int]
    buff_list: Optional[List[Buff]]  # optional for easy input


@dataclass
class SpBuff(Buff):
    buffs: List[Buff]


@dataclass
class Np:
    card: str
    name: str
    icon: str
    rank: str
    type: str
    type_flag: str
    detail: str
    distribution: List[int]
    priority: int


@dataclass
class Servant(ServantInput):
    np_gain: int
    np_gain_hit: int

    skills: Dict
    # np: List[Np]
