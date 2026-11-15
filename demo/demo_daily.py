# -*- coding: utf-8 -*-
"""通用引擎 demo —— 用「光 / 影」这个领域跑一遍新架构。

演示四件事：
    1. 一个元素 = 本有含义 + 本有属性
    2. 两个元素 → 后有含义 / 状态
    3. 双集合体 → 即时状态
    4. 聚（≥3 集合体）与 散（状态散入 → 后有含义）

运行：
    cd repo/demo && python demo_daily.py

引擎里没有一个「光/影」之外的领域词 —— 换领域，只换这本字典。
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))

from engine import (  # noqa: E402
    Element, Attribute, Collection, DualCollection,
    judge, post_meaning, merge, seep,
)

# ── 这个领域的字典：光 / 影 ─────────────────────────────
LIGHT = Element("明亮", Attribute.YANG, "光")
SHADOW = Element("遮蔽", Attribute.YIN, "影")
DAWN = Element("初起", Attribute.YANG, "晨")
DUSK = Element("沉落", Attribute.YIN, "暮")


def line(title):
    print("\n" + "─" * 56)
    print(title)
    print("─" * 56)


def main():
    line("① 单元素：含义 + 属性")
    for e in (LIGHT, SHADOW, DAWN, DUSK):
        print(f"  {e.name:<4} 本有含义={e.meaning:<4} 本有属性={e.attr.value}")

    line("② 两个元素：后有含义 与 状态")
    st = judge(LIGHT.attr, SHADOW.attr)
    pm = post_meaning(LIGHT, SHADOW, rule=lambda a, b: f"{a}被{b}压住，成了“明暗交界”")
    print(f"  光 × 影 → 状态={st.value}")
    print(f"           后有含义={pm.text}")

    line("③ 双集合体：即时状态")
    c1 = Collection([LIGHT, DAWN], "晨光")
    c2 = Collection([SHADOW, DUSK], "暮影")
    dual = DualCollection(c1, c2)
    print("  晨光 × 暮影 → 即时状态:",
          [s.value for s in dual.instant_states()])

    line("④ 聚：三个以上集合体，本有状态重叠")
    c3 = Collection([Element("温暖", Attribute.YANG), Element("上升", Attribute.YANG)], "暖阳")
    hs = merge([c1, c3, Collection([DAWN, LIGHT], "初亮")], direction="向外扩散")
    print("  ", hs.describe() if hs else "未成立（没有共同的本有状态）")

    line("⑤ 散：状态散入另一个集合体 → 后有含义")
    flows = seep(c1, [c3])
    if not flows:
        print("  没有可配的状态")
    for f in flows:
        print(f"  {c1.name} → {f.target.name}　状态={f.state.value}")
        print(f"    得到后有含义：{f.post.text if f.post else '—'}")


if __name__ == "__main__":
    main()
