# Enterprise Python for Java Developers

A hands-on, time-boxed course for experienced Java engineers who need to **read, understand, review, and write enterprise Python**.

This repository is both a learning course and an evolving pet project suitable for GitHub.

## Start here

Open:

**`ENTERPRISE_PYTHON_COURSE.md`**

That file is the single source of truth.

Use `PROGRESS.md` to track planned vs actual time.

## How ChatGPT fits in

You should not need chat to know what comes next.

Use chat only for:

- conceptual questions;
- TODO/code review;
- failing tests;
- checkpoint review.

## Current baseline

Module 1 is already implemented.

Run:

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\Activate.ps1   # Windows PowerShell

python -m pip install --upgrade pip
pip install -e ".[dev]"
pytest -q
```

The broad `except Exception` in `OrderService` is intentional and becomes a teaching target in Module 3.

## GitHub

The course contains explicit **COMMIT** and **COMMIT + PUSH** gates.

Do not commit every tiny edit. Commit coherent tested states; push milestone states.
