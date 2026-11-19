# -*- coding: utf-8 -*-
"""关系推导法 · 通用引擎

只认三样东西：含义、属性、状态。不认识任何具体领域。

    元素      = 本有含义 + 本有属性
    组合      = 两个元素放一起
                本有含义 × 本有含义 → 后有含义
                本有属性 × 本有属性 → 状态
    集合体    = 多个元素形成的一个整体
    聚        = 三个以上集合体，各自的本有状态一对一配对 → 隐形集合
    散        = 一个集合体的状态散入另一个 → 产生后有含义

唯一的硬要求：每一步都能回溯。
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


# ═══════════════════════════════════════════════════════════════
# 一、属性与状态
# ═══════════════════════════════════════════════════════════════

class Attribute(Enum):
    """默认档位：阴 / 阳 / 中。

    ★ 档位不是固定的：任何领域都可以用自己的质化档位（冷/温/热、向内/中立/向外），
      但必须同时提供对应的状态表 —— 见 Profile。
    """
    YIN = "阴"
    YANG = "阳"
    NEUTRAL = "中"


class State(Enum):
    """两个属性放在一起得到的状态。"""
    CONFLICT = "对碰"      # 相对、矛盾
    OVERLAP = "重叠"       # 相关、和谐
    HARMONY = "交汇"       # 留白、可供选择
    NONE = "无状态"        # 没配成组合


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
# ─────────────────────────────────────────────────────────────

# 基础关系表（6 行）—— 系统只用这一张，不做七档进阶
BASIC_TABLE = {
    frozenset(("阴", "阳")): State.CONFLICT,
    frozenset(("阴", "阴")): State.OVERLAP,
    frozenset(("阳", "阳")): State.OVERLAP,
    frozenset(("中", "阴")): State.HARMONY,
    frozenset(("中", "阳")): State.HARMONY,
    frozenset(("中", "中")): State.OVERLAP,
}


@dataclass
class Profile:
    """一套档位配置：档位名单 + 对应的状态表。

    换档位 = 换 Profile；档位变了，状态表必须跟着换——
    否则「阴/阳/中」的表拿去查「冷/温/热」，出来的状态是错的。
    """
    name: str
    tiers: List[str]
    table: Dict[frozenset, State]

    def state_of(self, a, b) -> State:
        return self.table.get(frozenset((a, b)), State.NONE)


DEFAULT_PROFILE = Profile(
    name="阴 / 阳 / 中",
    tiers=["阴", "阳", "中"],
    table={
        frozenset(("阴", "阳")): State.CONFLICT,
        frozenset(("阴", "阴")): State.OVERLAP,
        frozenset(("阳", "阳")): State.OVERLAP,
        frozenset(("中", "阴")): State.HARMONY,
        frozenset(("中", "阳")): State.HARMONY,
        frozenset(("中", "中")): State.OVERLAP,
    },
)


def fold(attr, intensity: str = ""):
    """把带强度的属性折回三性。判定前必须先折。"""
    return attr


def with_intensity(meaning: str, intensity: str) -> str:
    """强度只影响含义的写法，不影响状态。"""
    if intensity == "极":
        return f"{meaning}（过度）"
    if intensity == "衰":
        return f"{meaning}（不足）"
    return meaning


def judge(attr_a, attr_b, table=None, profile: Optional[Profile] = None) -> State:
    """两个档位 → 状态。唯一真正的「计算」。

    三种用法：
        judge(a, b)                       # 用默认 阴/阳/中 + 6 行表
        judge(a, b, profile=P)            # 换成某个领域自己的档位与表
        judge(a, b, table={...})          # 只换表
    档位可以是 Attribute 枚举，也可以是任意字符串。
    """
    if profile is not None:
        return profile.state_of(attr_a, attr_b)
    if table is None:
        ka = attr_a.value if isinstance(attr_a, Attribute) else attr_a
        kb = attr_b.value if isinstance(attr_b, Attribute) else attr_b
        return BASIC_TABLE.get(frozenset((ka, kb)), State.NONE)
    return table.get(frozenset((attr_a, attr_b)), State.NONE)


# ═══════════════════════════════════════════════════════════════
# 二、元素
# ═══════════════════════════════════════════════════════════════

@dataclass
class Element:
    """一个模糊个体：带一个本有含义、一个本有属性。"""
    meaning: str              # 本有含义
    attr: Any                 # 本有属性（Attribute 枚举，或领域自定义的字符串档位）
    name: str = ""            # 便于回溯的标识
    intensity: str = ""       # 强度："" / "极" / "衰"（只有颜色会带）

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


def post_meaning(a: Element, b: Element, rule=None) -> PostMeaning:
    """本有含义 × 本有含义 → 后有含义。

    rule 是领域给的合成函数：rule(a.meaning, b.meaning) -> str
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
    """集合体：多个元素形成的一个整体。

    内部元素两两判定的状态**全部列出**，不合并、不挑代表；
    等需要聚或散时，再和别的集合体一对一比对。
    """
    elements: List[Element] = field(default_factory=list)
    name: str = ""

    def states(self, table=None, profile=None) -> List[State]:
        out = []
        for i in range(len(self.elements)):
            for j in range(i + 1, len(self.elements)):
                out.append(judge(self.elements[i].attr,
                                 self.elements[j].attr, table, profile))
        return out

    def base_states(self, table=None, profile=None) -> List[State]:
        """本有状态：由「特定的双元素组合」产生；这里取全部内部状态。"""
        return self.states(table, profile)


@dataclass
class DualCollection:
    """双集合体：两个集合体之间 → 即时状态。"""
    a: Collection
    b: Collection

    def instant_states(self, table=None, profile=None) -> List[State]:
        out = []
        for ea in self.a.elements:
            for eb in self.b.elements:
                out.append(judge(ea.attr, eb.attr, table, profile))
        return out


# ═══════════════════════════════════════════════════════════════
# 四、聚与散
# ═══════════════════════════════════════════════════════════════

def _pair_up(lists: List[List[State]]) -> Dict[State, int]:
    """一对一配对：每个集合体拿出一个状态，用掉即止。

    返回 {状态: 能配上的对数}。
    没有就是没有，不强行凑。
    """
    if not lists:
        return {}
    common = set(lists[0]) - {State.NONE}
    for ls in lists[1:]:
        common &= set(ls)
    result: Dict[State, int] = {}
    for st in common:
        # 每个列表里这个状态有几个，取最小 → 能配几对
        result[st] = min(ls.count(st) for ls in lists)
    return {k: v for k, v in result.items() if v > 0}


@dataclass
class HiddenSet:
    """聚出来的隐形集合体。方向由使用的人决定。"""
    members: List[Collection]
    pairs: Dict[State, int]
    direction: str = ""       # ← 方向由人工需要决定，引擎不规定

    def describe(self) -> str:
        if not self.pairs:
            return "未成立"
        detail = "、".join(f"{k.value}×{v}" for k, v in self.pairs.items())
        d = f"，方向：{self.direction}" if self.direction else ""
        return f"{len(self.members)} 个集合体配对（{detail}）→ 隐形集合{d}"


def merge(collections: List[Collection], table=None, profile=None,
          direction: str = "") -> Optional[HiddenSet]:
    """聚：至少三个集合体，各自的本有状态一对一配对。

    匹配规则：只取「一个一个对得上」的状态，用掉即止；
    没有就是没有，不强行凑。集合体内部的状态全部列出，不挑代表。
    """
    if len(collections) < 3:
        return None
    pairs = _pair_up([c.base_states(table, profile) for c in collections])
    if not pairs:
        return None
    return HiddenSet(list(collections), pairs, direction)


@dataclass
class Seep:
    """散的一条边：从某个集合体散到另一个。"""
    source: Collection
    target: Collection
    state: State
    post: Optional[PostMeaning] = None


def seep(source: Collection, targets: List[Collection],
         table=None, profile=None, meaning_rule=None) -> List[Seep]:
    """散：一个集合体的状态，被散入另外的集合体 → 产生后有含义。

    前提：两边有相同、可一对一配上的本有状态。
    方向由使用的人决定（先选 source，再选 targets）。
    """
    src = [s for s in source.base_states(table, profile) if s != State.NONE]
    out: List[Seep] = []
    used = list(src)
    for t in targets:
        tgt = [s for s in t.base_states(table, profile) if s != State.NONE]
        shared = None
        for s in used:
            if s in tgt:
                shared = s
                break
        if shared is None:
            continue
        used.remove(shared)          # 用掉即止
        ea = source.elements[0] if source.elements else None
        eb = t.elements[0] if t.elements else None
        pm = post_meaning(ea, eb, meaning_rule) if (ea and eb) else None
        out.append(Seep(source=source, target=t, state=shared, post=pm))
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

    for f in seep(c1, [c2, c3]):
        print("散:", f.state.value, "→", f.post.text if f.post else "")
