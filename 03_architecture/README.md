# 03_architecture — Declarative Architecture Layer

This folder contains the **declarative architectural specification** of RAMORGA:
- C / G / S modules,
- the homeostatic meniscus,
- the field engine,
- regulatory flows and tension loops,
- high‑level system structure.

## Scope within this repository

The current repository — **ramorga-prototype** — provides:
- the five-module theoretical framework (01_theoretical_foundations),
- the declarative architecture layer (this folder),
- a minimal dynamic prototype (`ramorga_prototype.py`) implementing only
  the field dynamics loop (H–C/G/S–Meniscus).

This folder does **not** contain:
- module implementations,
- system interfaces,
- runtime logic,
- executable architecture components.

## Full architecture

The complete, production-level architecture (formal invariants, module contracts,
interfaces, diagrams, and system specifications) will be developed in a separate
repository:

**ramorga-architecture** *(in preparation)*

This folder therefore serves as a **structural placeholder** and a location for
declarative architectural documents, not executable components.
