# Relational Derivation

**A method that derives conclusions from relations** — not from intuition, and not from numbers. It works on two lines:

Split anything into a **meaning** (what it is like) and an **attribute** (which side it belongs to).
Meaning pairs with meaning to produce a new statement; attribute pairs with attribute to produce a relation state.

**What it does**

- Turns scattered material (card images, dreams, interviews, UI elements, team behaviour) into a **visible structure**
- Between two elements, derives a **state** (clash / overlap / meeting) — no free improvisation
- When three or more elements share the same state, they **join into one whole** (*merge*); a whole's state **seeps into another**, growing a new statement (*seep*)
- Every conclusion can be **traced back** to concrete elements: reproducible, traceable, refutable

**The one hard requirement: every step must be traceable.**
A conclusion points back to its elements; an element points back to its material. Nothing else is required.

**What it does not do**: no quantification (meaning cannot be measured) — **it only derives**; it does not predict and does not draw conclusions.

---

## How it works

Anything observable is first cut into **elements**. Each element carries exactly two things:

| | Question | Example |
|---|---|---|
| **Meaning** | What is it like? | "white" = pure, clean |
| **Attribute** | Which side is it on? | "white" = yang (outward, active) |

**The two halves travel separately from then on — neither speaks for the other.**

Put two elements together and both lines run at once:

```
meaning × meaning    → a new statement (post-meaning)
attribute × attribute → a relation state (clash / overlap / meeting)
```

---

## 1. Only four kinds of relation

> **Relation = the result of two things meeting on a dimension they share.**

There are only two such dimensions: **meaning** and **attribute**. Hence exactly four relations:

| Kind | Between | Direction | Produces |
|---|---|---|---|
| **Judging** | 2 elements (**attributes**) | symmetric | a **state** |
| **Composing** | 2 elements (**meanings**) | symmetric | a **post-meaning** |
| **Joining (merge)** | **3+** collections | undirected (a net) | an **implicit set** |
| **Seeping (seep)** | 1 → many collections | **one-way** | a **post-meaning** |

**Why exactly four**: only two things can be acted on (meaning / attribute), and only two scales (pair / many). 2 × 2 = 4.

---

## 2. How a domain closes the loop

A domain supplies seven things, in order — and must be able to **return to the raw material**:

```
1  Cutting     what counts as one element
2  Meaning     what each element is like
3  Attribute   which side each element belongs to (yin / yang / neutral)
4  Table       attribute × attribute → state  (usually the same 6-row table)
5  Collection  which elements form one collection
6  Merge/seep  which positions allow merging, which allow seeping
7  Output      how results become prose
```

**Four checks for a closed loop**

| Check | Meaning |
|---|---|
| **Traceable** | every conclusion points back to an element from step 1 |
| **Complete** | every element received a meaning and an attribute |
| **No blanks** | the judging table has no "undecidable" cell |
| **In bounds** | output introduces nothing beyond step 7 |

**Changing domain means replacing 1, 2, 5, 6, 7; step 4 usually stays.**

---

## 3. Four terms, kept apart

| Term | In one line |
|---|---|
| **intrinsic** | what the element already carries (meaning / attribute) |
| **post** | what exists only after two meanings meet |
| **instant state** | inside a dual collection: two attributes naturally produce it |
| **intrinsic state** | inside a single collection: produced by a specific two-element combination |

---

## 4. Where to read

| Order | File | Content |
|---|---|---|
| **1** | [docs/01_通用框架/基底方法论（文字）.md](docs/01_通用框架/基底方法论（文字）.md) | the methodology itself (Chinese) |
| **3** | [docs/01_通用框架/引擎分层说明.md](docs/01_通用框架/引擎分层说明.md) | engine layering + colour and intensity |
| 4 | [engine/engine.py](engine/engine.py) · [demo/demo_daily.py](demo/demo_daily.py) | the engine (no domain words) + a light/shadow demo |

---

## 5. Why there is no quantification

**Meaning cannot be measured.** Quantifying forces comparison by size, while "pure" and "warm" have no size relation.

So there are only three states plus "no state"; intensity acts on *meaning* (excessive / deficient), never on *state*.

**Its rigour does not come from numbers but from three things: reproducible, traceable, refutable.**

**Deriving is not predicting**: derivation lays out relations that already exist; it never claims what will happen.

---

## License

| Part | License |
|---|---|
| **Code** (`engine/`, `demo/`) | MIT — see [LICENSE](LICENSE) |
| **Docs and methodology** (`docs/`) | CC BY-NC 4.0 — see [LICENSE-docs](LICENSE-docs) |

**Commercial use of the documentation requires permission.**

---

## Contact

Questions, corrections, or applying it to your own domain — please open an [Issue](https://github.com/kite-y/relational-derivation/issues).

Or email: **zhiyuan_Y@outlook.com**


---

[中文](README.md) · **English**
