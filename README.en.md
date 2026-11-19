# Relational Derivation

[中文](README.md) · **English**

> A **qualitative method** that turns fuzzy material into **relations**, where every step can be traced back to its source.
> The repository holds the method itself, plus a runnable engine and an example.

---

## What this is

**Not intuition, and not numbers.** Two lines:

- Split anything into a **meaning** (what it is like) and an **attribute** (which side it belongs to)
- Meaning paired with meaning yields a **new statement**
- Attribute paired with attribute yields a **relation state** (clash / overlap / meeting)

**The one hard requirement: every step must be traceable.**
A conclusion points back to its elements; an element points back to its material.

| What it does | What it does not do |
|---|---|
| Turns scattered material (card images, dreams, interviews, UI elements, team behaviour) into a **visible structure** | **No quantification** (meaning cannot be measured) |
| Derives a **state** between two elements — no free improvisation | **No prediction** (it lays out existing relations only) |
| Joins three or more aligned states (**merge**); lets a whole's state seep elsewhere (**seep**) | **No conclusions where the material is silent** |

---

## Run it in three minutes

No third-party dependencies:

```bash
git clone https://github.com/kite-y/relational-derivation.git
cd relational-derivation/demo
python demo_daily.py
```

It runs a light/shadow example through five steps: single element → two elements → dual collection → merge → seep.

---

## How it works

| | Question | Example |
|---|---|---|
| **Meaning** | What is it like? | "white" = pure, clean |
| **Attribute** | Which side? | "white" = yang (outward, active) |

**The two halves travel separately — neither speaks for the other.**

---

## 1. Only four kinds of relation

> **Relation = the result of two things meeting on a dimension they share.**

Two dimensions only — **meaning** and **attribute** — hence exactly four relations:

| Kind | Between | Direction | Produces |
|---|---|---|---|
| **Judging** | 2 elements (attributes) | symmetric | a **state** |
| **Composing** | 2 elements (meanings) | symmetric | a **post-meaning** |
| **Joining (merge)** | 3+ collections | undirected | an **implicit set** |
| **Seeping (seep)** | 1 → many collections | one-way | a **post-meaning** |

---

## 2. How a domain closes the loop

A domain supplies seven things, in order, and must return to the raw material:

```
1  Cutting     what counts as one element
2  Meaning     what each element is like
3  Attribute   which side each element belongs to
4  Table       attribute × attribute → state (usually one 6-row table)
5  Collection  which elements form one collection
6  Merge/seep  which positions allow merging or seeping
7  Output      how results become prose
```

**Four checks**: traceable · complete · no blanks · in bounds.

---

## 3. Four terms

| Term | In one line |
|---|---|
| **intrinsic** | what the element already carries |
| **post** | what exists only after two meanings meet |
| **instant state** | produced naturally by two attributes in a dual collection |
| **intrinsic state** | produced by a specific two-element combination inside a collection |

---

## 4. Why there is no quantification

**Meaning cannot be measured.** Quantifying forces comparison by size, while "pure" and "warm" have no size relation.

So there are three states plus "no state"; intensity affects *meaning* only.

**Its rigour comes from being reproducible, traceable and refutable — not from numbers.**

> **Deriving is not predicting**: derivation lays out relations that already exist.

---

## 5. Branch: tarot

The method itself contains no domain. **For how a domain closes the loop, see the
[`tarot` branch](https://github.com/kite-y/relational-derivation/tree/tarot)** —
it fills in the seven steps and ships a complete example output.

---

## 6. Where to read

| Order | File | Content |
|---|---|---|
| **1** | [docs/01_通用框架/基底方法论（文字）.md](docs/01_通用框架/基底方法论（文字）.md) | the method itself (Chinese) |
| **2** | [docs/01_通用框架/引擎分层说明.md](docs/01_通用框架/引擎分层说明.md) | engine layering; colour and intensity |
| 3 | [engine/engine.py](engine/engine.py) | the engine (no domain words) |
| 4 | [demo/demo_daily.py](demo/demo_daily.py) | a light/shadow example |

---

## 7. License

**Dual license** — code and docs are separate.

| Part | License | File |
|---|---|---|
| **Code** (`engine/`, `demo/`) | **MIT** — commercial use allowed | [LICENSE](LICENSE) |
| **Docs and methodology** (`docs/`, README prose) | **CC BY-NC 4.0** — attribution, non-commercial | [LICENSE-docs](LICENSE-docs) |

**In one line**: use the code freely; the method and its text may be cited, adapted and taught, but not sold.

For commercial use of the documentation, email me.

---

## Contact

**Questions, discussion, or applying it to your own domain — all welcome.**

- **Issue**: https://github.com/kite-y/relational-derivation/issues
- **Email**: zhiyuan_Y@outlook.com
