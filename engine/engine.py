# -*- coding: utf-8 -*-
"""通用引擎 v3 —— 只认「含义 / 属性 / 状态」，不认识任何具体领域。

新架构（2026-11）：

    元素      = 本有含义 + 本有属性
    组合      = 两个元素放一起
                本有含义 × 本有含义 → 后有含义
                本有属性 × 本有属性 → 状态
    集合体    = 多个元素形成的一个整体（单集合体）
    双集合体  = 两个集合体
                属性 × 属性 → 即时状态
    聚        = 三个以上集合体，各自本有状态重叠 → 隐形集合（方向自定义）
    散        = 单集合体中的状态散入另外的集合体 → 产生后有含义

这一层不含任何领域词：颜色、牌名、方位都不出现。
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


# ═══════════════════════════════════════════════════════════════
# 一、属性与状态（领域给表，引擎只管查）
# ═══════════════════════════════════════════════════════════════

class Attribute(Enum):
    """属性只有三性：阴 / 阳 / 中。不做七档，不做量化。"""
    YIN = "阴"
    YANG = "阳"
    NEUTRAL = "中"


class State(Enum):
    """两个属性放在一起得到的状态。"""
    CONFLICT = "对碰"      # 相对、矛盾
    OVERLAP = "重叠"       # 相关、和谐
    HARMONY = "交汇"       # 留白、可供选择
    NONE = "无状态"        # 没配成组合


# 领域把「属性1 × 属性2 → 状态」的表交给引擎；引擎不内置任何表。
_BaseTable = Dict[frozenset, State]


def judge(attr_a: Attribute, attr_b: Attribute,
          table: Optional[_BaseTable] = None) -> State:
    """两个属性 → 状态。唯一真正的「计算」。

    没有给表时用最小默认表（阴/阳/中 三档），领域可以整张替换。
    """
    if table is None:
        return _default_judge(attr_a, attr_b)
    key = frozenset((attr_a, attr_b))
    return table.get(key, State.NONE)


# ─────────────────────────────────────────────────────────────
# 颜色与强度（唯一带强度的类别）
#
#  只有「颜色」会带强度：极（过度）/ 衰（不足）/ 无。
#
#  处理顺序（不能乱）：
#    ① 先得到变化的强度
#         深浅（单个颜色）：深 → 极　　浅 → 衰
#         对立（两个颜色）：少数几对合法，成立才给强度
#    ② 用强度改写「含义」        → with_intensity()
#    ③ 折回三性（判定前必须做）   → fold()
#    ④ 再判定状态               → judge()
#
#  ★ 强度只走“含义”这条路，不进“状态”这条路。
#  ★ 状态没有强度：不存在「强对碰 / 弱重叠」。
#  ★ 强度不改锚点，也不叠加（极再极还是极）。
#  ★ 写了“过度/不足”，要能回溯到是哪次深浅 / 哪一对对立造成的。
# ─────────────────────────────────────────────────────────────


def fold(attr: Attribute, intensity: str = "") -> Attribute:
    """把带强度的属性折回三性。判定前必须先折。"""
    return attr          # 三性本身不随强度改变，保留此函数作为显式步骤


def with_intensity(meaning: str, intensity: str) -> str:
    """强度只影响含义的写法，不影响状态。"""
    if intensity == "极":
        return f"{meaning}（过度）"
    if intensity == "衰":
        return f"{meaning}（不足）"
    return meaning


# 基础关系表（6 行）—— 系统只用这一张，不做七档进阶
BASIC_TABLE = {
    frozenset((Attribute.YIN, Attribute.YANG)): State.CONFLICT,
    frozenset((Attribute.YIN, Attribute.YIN)): State.OVERLAP,
    frozenset((Attribute.YANG, Attribute.YANG)): State.OVERLAP,
    frozenset((Attribute.NEUTRAL, Attribute.YIN)): State.HARMONY,
    frozenset((Attribute.NEUTRAL, Attribute.YANG)): State.HARMONY,
    frozenset((Attribute.NEUTRAL, Attribute.NEUTRAL)): State.OVERLAP,
}


def _default_judge(a: Attribute, b: Attribute) -> State:
    return BASIC_TABLE.get(frozenset((a, b)), State.NONE)


# ═══════════════════════════════════════════════════════════════
# 二、元素
# ═══════════════════════════════════════════════════════════════

@dataclass
class Element:
    """一个模糊个体：带一个本有含义、一个本有属性。"""
    meaning: str              # 本有含义
    attr: Attribute           # 本有属性
    name: str = ""            # 便于回溯的标识（颜色名、物件名……）
    intensity: str = ""       # 强度："" 无 / "极" / "衰"（见下「颜色与强度」）

    def __post_init__(self):
        if not self.name:
            self.name = self.meaning


@dataclass
class PostMeaning:
    """后有含义：两个本有含义交互之后才有的东西。"""
    from_a: str
    from_b: str
    text: str

    @property
    def sources(self):
        return (self.from_a, self.from_b)


def post_meaning(a: Element, b: Element,
                 rule=None) -> PostMeaning:
    """本有含义 × 本有含义 → 后有含义。

    rule 是领域给的合成函数：rule(a.meaning, b.meaning) -> str
    没给时用最朴素的说法，保证调用链能走通。
    """
    if rule is not None:
        text = rule(a.meaning, b.meaning)
    else:
        text = f"{a.meaning} 与 {b.meaning} 相互之后"
    return PostMeaning(a.meaning, b.meaning, text)


# ═══════════════════════════════════════════════════════════════
# 三、集合体
# ═══════════════════════════════════════════════════════════════

@dataclass
class Collection:
    """单集合体：多个元素形成的一个整体。"""
    elements: List[Element] = field(default_factory=list)
    name: str = ""

    def states(self, table=None) -> List[State]:
        """它内部两两判定出来的状态。"""
        out = []
        for i in range(len(self.elements)):
            for j in range(i + 1, len(self.elements)):
                out.append(judge(self.elements[i].attr,
                                 self.elements[j].attr, table))
        return out

    def base_states(self, table=None) -> List[State]:
        """本有状态：由「特定的双元素组合」产生 —— 领域指定哪几对。"""
        return self.states(table)


@dataclass
class DualCollection:
    """双集合体：两个集合体之间。"""
    a: Collection
    b: Collection

    def instant_states(self, table=None) -> List[State]:
        """即时状态：两个集合体的属性自然产生的状态。"""
        out = []
        for ea in self.a.elements:
            for eb in self.b.elements:
                out.append(judge(ea.attr, eb.attr, table))
        return out


# ═══════════════════════════════════════════════════════════════
# 四、聚与散
# ═══════════════════════════════════════════════════════════════

@dataclass
class HiddenSet:
    """聚出来的隐形集合体。方向由调用方自定义。"""
    members: List[Collection]
    shared_state: State
    direction: str = ""       # ← 方向自定义，引擎不规定

    def describe(self) -> str:
        return (f"{len(self.members)} 个集合体因「{self.shared_state.value}」"
                f"连成隐形集合" + (f"，方向：{self.direction}" if self.direction else ""))


def merge(collections: List[Collection], table=None,
          direction: str = "") -> Optional[HiddenSet]:
    """聚：至少三个集合体，各自的本有状态形成重叠态。

    条件：三者的本有状态必须有共同的「重叠」 —— 也就是说
    每个集合体都能拿出一个相同的本有状态。
    """
    if len(collections) < 3:
        return None

    pools = [set(c.base_states(table)) for c in collections]
    shared = set.intersection(*pools) if pools else set()
    shared.discard(State.NONE)
    if not shared:
        return None
    # 优先重叠
    chosen = State.OVERLAP if State.OVERLAP in shared else sorted(shared, key=lambda s: s.value)[0]
    return HiddenSet(list(collections), chosen, direction)


@dataclass
class Seep:
    """散的一条边：从某个集合体散到另一个。"""
    source: Collection
    target: Collection
    state: State
    post: Optional[PostMeaning] = None


def seep(source: Collection, targets: List[Collection],
         table=None, meaning_rule=None) -> List[Seep]:
    """散：单集合体中的状态，被散入另外的集合体 → 产生后有含义。

    前提：两边有相同的本有状态。一条状态散出去，就在对家产生一条后有含义。
    """
    src_states = set(source.base_states(table))
    src_states.discard(State.NONE)

    out: List[Seep] = []
    for t in targets:
        tgt_states = set(t.base_states(table))
        tgt_states.discard(State.NONE)
        shared = src_states & tgt_states
        if not shared:
            continue
        st = State.OVERLAP if State.OVERLAP in shared else sorted(shared, key=lambda s: s.value)[0]

        ea = source.elements[0] if source.elements else None
        eb = t.elements[0] if t.elements else None
        pm = post_meaning(ea, eb, meaning_rule) if (ea and eb) else None
        out.append(Seep(source=source, target=t, state=st, post=pm))
    return out


# ═══════════════════════════════════════════════════════════════
# 五、最小自检
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    a = Element("纯粹", Attribute.YANG, "白")
    b = Element("混沌", Attribute.YIN, "黑")
    print("判定:", judge(a.attr, b.attr).value)
    print("后有含义:", post_meaning(a, b).text)

    c1 = Collection([a, Element("冷静", Attribute.YANG, "白2")], "集合体1")
    c2 = Collection([Element("暖", Attribute.YANG), Element("丰盛", Attribute.YANG)], "集合体2")
    c3 = Collection([Element("生长", Attribute.YANG), Element("向上", Attribute.YANG)], "集合体3")

    hs = merge([c1, c2, c3], direction="向外")
    print("聚:", hs.describe() if hs else "未成立")

    flows = seep(c1, [c2, c3])
    for f in flows:
        print("散:", f.state.value, "→", f.post.text if f.post else "")
