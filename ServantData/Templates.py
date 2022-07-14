from dataclasses import dataclass, field
from dacite import from_dict
from typing import Optional, List, Union, Dict


@dataclass
class FunctionSvals:
    Rate: List[int]  # Exception: 83 Solomon
    Turn: Optional[List[int]]
    Count: Optional[List[int]]
    Value: Optional[List[int]]
    Value2: Optional[List[int]]

    ActSet: Optional[List[int]]
    ActSetWeight: Optional[List[int]]
    AddIndividualty: Optional[List[int]]
    AddLinkageTargetIndividualty: Optional[List[int]]
    AuraEffectId: Optional[List[int]]
    #DependFuncId: Optional[List[int]]
    #DependFuncVals: Optional[List[int]]
    HideMiss: Optional[List[int]]
    HideNoEffect: Optional[List[int]]
    InvalidHide: Optional[List[int]]
    MotionChange: Optional[List[int]]
    ParamAdd: Optional[List[int]]
    ParamMax: Optional[List[int]]
    RatioHPHigh: Optional[List[int]]
    RatioHPLow: Optional[List[int]]
    RatioHPRangeHigh: Optional[List[int]]
    RatioHPRangeLow: Optional[List[int]]
    ShowCardOnly: Optional[List[int]]
    ShowQuestNoEffect: Optional[List[int]]
    ShowState: Optional[List[int]]
    SkillID: Optional[List[int]]
    SkillLV: Optional[List[int]]
    StarHigher: Optional[List[int]]
    UseRate: Optional[List[int]]


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
    buff_list: List[Buff] = field(init=False)


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
class Servant():
    id: int
    collectionNo: int
    name: str
    className: str
    rarity: int
    cost: int
    attribute: str
    starAbsorb: int
    starGen: int
    instantDeathChance: int
    cards: List[str]
    hitsDistribution: Dict
    atkBase: int
    atkMax: int
    hpBase: int
    hpMax: int
    # atkGrowth: List[int]
    # hpGrowth: List[int]
    # bondGrowth: List[int]
    # expGrowth: List[int]
    np_gain: int = field(init=False)
    np_gain_hit: int = field(init=False)

    skill: Dict = field(init=False)
    # np: List[Np] = field(init=False)
