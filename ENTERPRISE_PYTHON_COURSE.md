# Enterprise Python for Java Developers

## Purpose

This course is designed for an experienced Java engineer who needs to become productive in **enterprise Python codebases**, not merely learn beginner Python syntax.

You will use one evolving Order Service.

The goal is to be able to open a real Python backend and understand:

- where execution starts;
- how objects and types behave;
- how dependencies are wired;
- how interfaces/contracts are represented;
- how errors propagate;
- how decorators and context managers change behavior;
- how iterators/generators differ from collections;
- how async I/O works;
- how tests are structured;
- how FastAPI, Pydantic, SQLAlchemy, configuration, logging, Docker, and CI fit together.

---

# How to use this course

## Rule 1 — This file is the source of truth

Do not use old chat messages to determine what comes next.

Work through this file from top to bottom.

## Rule 2 — Time yourself

For every module:

1. record the start time in `PROGRESS.md`;
2. run a timer only while actively learning/coding;
3. record actual focused minutes;
4. compare actual vs planned time.

The time boxes are a diagnostic tool, not an exam.

## Rule 3 — Follow the six-step loop

Every module follows:

**READ → UNDERSTAND → CHANGE → RUN → GIT GATE → STOP**

Do not skip directly to the implementation.

## Rule 4 — Use ChatGPT as a reviewer, not as the course navigator

Return to chat only when:

- a concept is unclear;
- a test fails and you cannot explain why;
- you want a TODO reviewed;
- you want confirmation before crossing a Git gate.

Recommended format:

```text
M4-T2 complete.

Code:
...

Tests:
...

My understanding:
...

Please review.
```

## Rule 5 — Do not read future solutions

This repository does not contain final implementations for future modules.

You should write them.

---

# Course map

## Core crash course — 60 focused minutes

| Module | Planned | Main concept | Java anchor |
|---|---:|---|---|
| M1 | 15 min | domain, type hints, `self`, DI, Protocol | record/POJO, interface, constructor injection |
| M2 | 10 min | object model, collections, mutability | object references, List/Map/Set |
| M3 | 10 min | exceptions and boundaries | exception hierarchy |
| M4 | 10 min | decorators and context managers | AOP/interceptor + try-with-resources |
| M5 | 8 min | iteration and generators | Iterable/Stream |
| M6 | 7 min | async recognition and request tracing | CompletableFuture/non-blocking I/O |

After M6, you should be able to **read** a well-structured Python service without being blocked by Python syntax.

## Enterprise build track — about 5 hours 10 minutes

| Module | Planned | Outcome |
|---|---:|---|
| M7 | 35 min | pytest fixtures, fakes, mocks, parametrization |
| M8 | 60 min | FastAPI + Pydantic HTTP service |
| M9 | 35 min | configuration + structured logging |
| M10 | 75 min | SQLAlchemy + PostgreSQL persistence |
| M11 | 45 min | async external payment client |
| M12 | 60 min | Docker, CI, packaging, GitHub presentation |

---

# M1 — Domain, types, DI, Protocol

**Planned time: 15 minutes**

**Status in this bundle: COMPLETE BASELINE**

You have already implemented `OrderService.create_order()`.

## READ

Inspect:

```text
src/acme_orders/domain.py
src/acme_orders/ports.py
src/acme_orders/repository.py
src/acme_orders/payment.py
src/acme_orders/service.py
```

## UNDERSTAND

You should be able to explain:

```python
def create_order(self, customer_id: str, amount: Decimal) -> Order:
```

as:

- `def` — method/function definition;
- `self` — current instance, broadly analogous to Java `this`;
- `customer_id: str` — parameter type hint;
- `amount: Decimal` — parameter type hint;
- `-> Order` — return type hint.

You should also be able to explain:

- `Order` as an immutable dataclass/value object;
- `OrderService` as business/application logic;
- `OrderRepository` as a port/contract;
- `PaymentGateway` as a port/contract;
- `InMemoryOrderRepository` and `FakePaymentGateway` as concrete adapters/implementations.

## RUN

```bash
pytest -q
```

Expected:

```text
3 passed
```

## M1 CHECKPOINT

Before continuing, answer without looking anything up:

1. Why is `OrderRepository` not the database itself?
2. Why can `OrderService` accept a repository implementation without constructing it?
3. What does `Order | None` mean?
4. What is the rough Java equivalent of `-> None`?
5. Why is `ports.py` an architectural name rather than a Python requirement?

If you cannot answer at least 4/5, revisit M1 before moving on.

## GIT GATE — COMMIT + PUSH

This is a coherent baseline and should exist remotely before further refactoring.

If this is a brand-new repository:

```bash
git init
git add .
git commit -m "feat: establish typed order service baseline"
git branch -M main
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin main
```

If the remote already exists:

```bash
git add .
git commit -m "feat: establish typed order service baseline"
git push
```

**Gate opens only if `pytest -q` passes.**

---

# M2 — Python object model and collections

**Planned time: 10 minutes**

## Goal

Stop translating every Python object into Java syntax and start recognizing the Python runtime model.

You will touch:

- `list`
- `dict`
- `set`
- `tuple`
- mutability
- references
- `None`
- comprehensions

## Java map

| Python | Java mental model |
|---|---|
| `list[Order]` | `List<Order>` |
| `dict[str, Order]` | `Map<String, Order>` |
| `set[str]` | `Set<String>` |
| `tuple[str, int]` | fixed positional values |
| `None` | closest everyday analogy is `null` |
| comprehension | concise collection transformation/filtering |

## READ

Open:

```text
src/acme_orders/repository.py
```

Study:

```python
self._orders: dict[str, Order] = {}
```

Understand that the repository is currently an in-memory map:

```text
order id -> Order
```

## CHANGE — M2-T1

Add this method to `InMemoryOrderRepository`:

```python
def find_all(self) -> list[Order]:
    ...
```

Return all currently stored orders.

Do **not** expose the internal dictionary itself.

Before coding, answer:

> Why would `return self._orders` be a bad abstraction?

## CHANGE — M2-T2

Add:

```python
def find_customer_ids(self) -> set[str]:
    ...
```

Return unique customer IDs.

Try using a **set comprehension**.

## CHANGE — M2-T3

Add:

```python
def order_summaries(self) -> list[tuple[str, Decimal]]:
    ...
```

Return:

```text
[(customer_id, amount), ...]
```

Try using a **list comprehension**.

## ADD TESTS

Add tests proving:

- `find_all()` returns all saved orders;
- duplicate customer IDs become one entry in `find_customer_ids()`;
- summaries contain expected `(customer_id, amount)` pairs.

## RUN

```bash
pytest -q
```

## CHECKPOINT

Explain the difference between:

```python
orders = repository.find_all()
```

and:

```python
orders = repository._orders
```

especially regarding abstraction and mutability.

## GIT GATE — COMMIT

```bash
git add .
git commit -m "feat: add collection-based repository queries"
```

Do not push yet.

## STOP

If you finished under 10 minutes, explain a list comprehension aloud before continuing.

If you exceeded 15 minutes, record which concept caused the slowdown.

---

# M3 — Exceptions and enterprise boundaries

**Planned time: 10 minutes**

## Goal

Learn why exception handling is an architectural concern, not merely syntax.

## Java anchor

This is suspicious in Java:

```java
catch (Exception e) {
    throw new ValidationException(...);
}
```

The equivalent Python smell is already present in your service.

## READ

Open:

```text
src/acme_orders/service.py
```

Find:

```python
except Exception as exc:
    raise OrderValidationError(f"Payment failed: {exc}")
```

Identify two problems before changing it.

Expected direction:

1. not every failure is validation;
2. repository failure is not necessarily payment failure.

## CHANGE — M3-T1

In `domain.py`, add:

```python
class PaymentError(RuntimeError):
    pass


class OrderPersistenceError(RuntimeError):
    pass
```

## CHANGE — M3-T2

In `payment.py`, create a gateway-specific failure path.

For this course, make the fake gateway raise `PaymentError` when:

```text
customer_id == "payment-failure"
```

## CHANGE — M3-T3

Refactor `OrderService.create_order()` so that:

- validation failures remain `OrderValidationError`;
- payment failures remain `PaymentError`;
- repository failures become `OrderPersistenceError`;
- unexpected exceptions are not mislabeled as validation errors.

Use Python exception chaining where appropriate:

```python
raise SomeError("message") from exc
```

## TEST

Write one test for each error category.

## RUN

```bash
pytest -q
```

## CHECKPOINT

Explain why this distinction matters for:

- HTTP status mapping;
- retry decisions;
- logging/alerts;
- client-visible errors.

## GIT GATE — COMMIT

```bash
git add .
git commit -m "refactor: introduce explicit service error boundaries"
```

Do not push yet.

---

# M4 — Decorators and context managers

**Planned time: 10 minutes**

## Goal

Recognize two Python mechanisms heavily used by frameworks.

## Part A — Decorators

Study:

```python
@audit
def create_order(...):
```

Mentally translate:

```python
create_order = audit(create_order)
```

Java anchor:

- Spring AOP;
- method interceptor;
- annotation-driven cross-cutting concern.

## CHANGE — M4-T1

Improve `audit()` so that it:

- preserves the original function name using `functools.wraps`;
- reports success when the function succeeds;
- reports failure when an exception occurs;
- re-raises the original exception.

Do not swallow exceptions.

## Part B — Context managers

Study:

```text
src/acme_orders/utils.py
```

Then write a test or tiny script using:

```python
with transaction("create-order"):
    service.create_order(...)
```

Java anchor:

- try-with-resources;
- transaction/resource lifetime;
- `finally`-style cleanup.

## CHANGE — M4-T2

Change `transaction()` so the caller can observe BEGIN/COMMIT/ROLLBACK via logging or a supplied callback rather than relying only on hard-coded `print`.

Keep it simple.

## RUN

```bash
pytest -q
```

## GIT GATE — COMMIT + PUSH

```bash
git add .
git commit -m "feat: improve auditing and transaction boundaries"
git push
```

---

# M5 — Iteration and generators

**Planned time: 8 minutes**

## Goal

Understand code that processes data lazily.

## Java anchor

Think:

```java
Iterable<Order>
Stream<Order>
```

rather than:

```java
List<Order>
```

## CHANGE — M5-T1

Add to `InMemoryOrderRepository`:

```python
def iter_orders(self):
    ...
```

Use `yield`.

Do not first build another list.

## CHANGE — M5-T2

Write:

```python
def iter_large_orders(orders, minimum: Decimal):
    ...
```

Use a generator to yield only matching orders.

Add type hints.

## TEST

Prove that `iter_orders()` is lazy/iterator-like rather than a pre-built list.

Do not overfit the test to a private implementation detail.

## CHECKPOINT

Explain:

- what `yield` does;
- why lazy iteration can reduce memory usage;
- when returning a normal list is still preferable.

## GIT GATE — COMMIT

```bash
git add .
git commit -m "feat: add lazy order iteration"
```

Do not push yet.

---

# M6 — Async recognition and end-to-end tracing

**Planned time: 7 minutes**

This module is about **reading and mental models**, not building production async code yet.

## CHANGE — M6-T1

Create:

```text
src/acme_orders/async_demo.py
```

Implement:

```python
import asyncio


async def fetch_risk_score(customer_id: str) -> int:
    await asyncio.sleep(0.05)
    return 10


async def demo() -> None:
    score = await fetch_risk_score("cust-1")
    print(score)


if __name__ == "__main__":
    asyncio.run(demo())
```

Run:

```bash
python -m acme_orders.async_demo
```

## UNDERSTAND

When you see:

```python
async def
await
```

think:

> This function participates in asynchronous execution and can yield control while waiting on I/O.

Do **not** equate it mechanically to "new thread".

Java anchors:

- `CompletableFuture`;
- asynchronous I/O;
- reactive/non-blocking service concepts.

## TRACE THE APPLICATION

Without running anything, trace:

```text
test
  -> OrderService
      -> PaymentGateway
      -> OrderRepository
          -> Order
```

Write a five-sentence explanation in your notes.

## GIT GATE — COMMIT + PUSH

```bash
git add .
git commit -m "docs: complete core Python execution model exercises"
git push
```

## CORE 60 CHECKPOINT

At this point you should recognize:

- `def`
- `self`
- `__init__`
- type hints
- `Protocol`
- `None`
- `Order | None`
- exceptions
- decorators
- context managers
- comprehensions
- generators
- `async` / `await`
- pytest basics

If three or more remain unclear, revise before M7.

---

# M7 — pytest, fixtures, fakes, mocks

**Planned time: 35 minutes**

## Goal

Move from "tests pass" to understanding how Python services are isolated and verified.

## Java anchors

| pytest concept | Java anchor |
|---|---|
| test function | JUnit test method |
| fixture | reusable test setup |
| fake | handwritten implementation |
| mock | Mockito-like interaction verification |
| parametrization | parameterized tests |

## READ

Study:

```python
@pytest.fixture
def service() -> OrderService:
```

## CHANGE — M7-T1

Create a fake repository in the test module that records saved orders.

Do not inherit from `OrderRepository`.

Use it successfully with `OrderService`.

This demonstrates structural typing.

## CHANGE — M7-T2

Use `pytest-mock` to verify:

- `payment_gateway.charge(...)` is called once;
- repository `save(...)` is called once.

## CHANGE — M7-T3

Use:

```python
@pytest.mark.parametrize(...)
```

to test several invalid amounts.

## RUN

```bash
pytest -q
```

## GIT GATE — COMMIT

```bash
git add .
git commit -m "test: expand service tests with fixtures fakes and mocks"
```

---

# M8 — FastAPI and Pydantic

**Planned time: 60 minutes**

## Goal

Expose the service over HTTP.

Java anchors:

- FastAPI ≈ Spring MVC/Spring Web conceptually;
- Pydantic model ≈ validated request/response DTO;
- dependency function ≈ lightweight dependency provider.

## DEPENDENCIES

Add to `pyproject.toml`:

```text
fastapi
uvicorn
httpx
```

Then:

```bash
pip install -e ".[dev]"
```

## CREATE

Suggested files:

```text
src/acme_orders/api.py
src/acme_orders/schemas.py
src/acme_orders/app.py
```

## M8-T1 — Request/response models

Create:

```text
CreateOrderRequest
OrderResponse
```

Check how `Decimal` is serialized rather than assuming.

## M8-T2 — HTTP endpoints

Implement:

```text
POST /orders
GET /orders/{order_id}
```

Map domain/service exceptions to appropriate HTTP responses.

## M8-T3 — API tests

Test:

- successful creation;
- invalid request;
- missing order;
- payment failure.

## RUN

Run tests, then:

```bash
uvicorn acme_orders.app:app --reload
```

Inspect `/docs`.

## CHECKPOINT

Trace:

```text
HTTP request
 -> Pydantic validation
 -> endpoint
 -> OrderService
 -> port
 -> adapter
 -> HTTP response
```

## GIT GATE — COMMIT + PUSH

```bash
git add .
git commit -m "feat: expose order service through FastAPI"
git push
```

---

# M9 — Configuration and logging

**Planned time: 35 minutes**

## Goal

Remove hard-coded operational behavior.

Java anchors:

- Spring `application.yml`;
- environment-based configuration;
- SLF4J/logback.

## M9-T1

Create an application settings model.

Support at least:

```text
APP_ENV
LOG_LEVEL
```

Do not commit `.env`.

## M9-T2

Replace `print()` auditing/transaction output with Python `logging`.

Use module-level loggers:

```python
import logging

logger = logging.getLogger(__name__)
```

## M9-T3

Make logs useful for tracing order creation.

Avoid logging secrets or full payment data.

## RUN

```bash
pytest -q
```

Launch the app and inspect logs.

## GIT GATE — COMMIT

```bash
git add .
git commit -m "feat: add environment configuration and application logging"
```

---

# M10 — SQLAlchemy and PostgreSQL

**Planned time: 75 minutes**

## Goal

Replace the in-memory adapter with real persistence while keeping the service dependent on the port.

Java anchor:

- SQLAlchemy ORM ≈ JPA/Hibernate conceptually;
- repository adapter ≈ persistence implementation.

## Architecture target

```text
OrderService
      |
      v
OrderRepository  <-- port
      ^
      |
SqlAlchemyOrderRepository
      |
      v
PostgreSQL
```

## M10-T1

Add SQLAlchemy dependencies.

Create persistence models separately from the domain model.

Before coding, answer:

> Why might the ORM entity and domain `Order` be separate types?

## M10-T2

Implement:

```text
SqlAlchemyOrderRepository
```

against the repository contract.

## M10-T3

Create integration tests.

The service itself should require minimal or no business-logic changes.

If replacing the repository forces a large rewrite of `OrderService`, diagnose the architecture before continuing.

## GIT GATE — COMMIT + PUSH

```bash
git add .
git commit -m "feat: add SQLAlchemy PostgreSQL persistence adapter"
git push
```

---

# M11 — Async external payment client

**Planned time: 45 minutes**

## Goal

Move from async recognition to a realistic outbound I/O boundary.

## Java anchor

Think asynchronous HTTP client / `CompletableFuture`, not raw thread creation.

## M11-T1

Create an async payment adapter using `httpx.AsyncClient`.

Do not call a paid external API.

Use a local/fake endpoint or mock transport.

## M11-T2

If payment becomes async, trace whether:

- only the adapter is async;
- the service becomes async;
- the FastAPI endpoint awaits the service.

Write the `await` chain explicitly.

## M11-T3

Test:

- successful async payment;
- timeout/failure;
- error translation at the service boundary.

## GIT GATE — COMMIT

```bash
git add .
git commit -m "feat: add asynchronous payment adapter"
```

---

# M12 — Docker, CI, packaging, and GitHub polish

**Planned time: 60 minutes**

## Goal

Turn the repository into a credible small portfolio project.

## M12-T1 — Docker

Create:

```text
Dockerfile
docker-compose.yml
```

Run:

```bash
docker compose up --build
```

The stack should eventually support API + PostgreSQL.

## M12-T2 — CI

Create:

```text
.github/workflows/tests.yml
```

On push / pull request:

- install Python;
- install dependencies;
- run tests.

Optional later additions:

- Ruff;
- mypy/pyright;
- coverage.

## M12-T3 — README polish

Rewrite `README.md` for a GitHub visitor.

It should explain:

1. what the project demonstrates;
2. architecture;
3. how to run it;
4. how to run tests;
5. main technologies;
6. design decisions.

Keep learning instructions in `ENTERPRISE_PYTHON_COURSE.md`.

## M12-T4 — Architecture document

Create:

```text
docs/ARCHITECTURE.md
```

Include:

```text
FastAPI
  |
OrderService
  |
Ports
 /   \
DB   Payment
```

Explain why adapters remain replaceable.

## FINAL RUN

```bash
pytest -q
docker compose up --build
```

Verify GitHub Actions after pushing.

## FINAL GIT GATE — COMMIT + PUSH

```bash
git add .
git commit -m "build: add Docker CI and project documentation"
git push
```

Optionally tag:

```bash
git tag -a v0.1.0 -m "Enterprise Python learning project v0.1.0"
git push origin v0.1.0
```

---

# Git strategy

## Commit rule

Commit when all are true:

- module behavior is complete;
- relevant tests pass;
- you can explain what changed;
- the commit has one coherent purpose.

## Push rule

Push at meaningful milestones:

1. baseline;
2. cross-cutting/core-language milestone;
3. Core 60 completion;
4. HTTP API;
5. real persistence;
6. final Docker/CI project.

## Example history

```text
feat: establish typed order service baseline
feat: add collection-based repository queries
refactor: introduce explicit service error boundaries
feat: improve auditing and transaction boundaries
feat: add lazy order iteration
docs: complete core Python execution model exercises
test: expand service tests with fixtures fakes and mocks
feat: expose order service through FastAPI
feat: add environment configuration and application logging
feat: add SQLAlchemy PostgreSQL persistence adapter
feat: add asynchronous payment adapter
build: add Docker CI and project documentation
```

---

# How to use ChatGPT

## Concept question

```text
Course M5:
I understand yield lazily produces values, but I don't understand how local variables are preserved between calls.
Explain using Java analogies.
```

## TODO review

```text
M3-T3 complete.

Implementation:
...

pytest:
...

Review it for correctness and enterprise Python style.
Do not give me the next module yet.
```

## Failure

```text
M8-T3

Command:
pytest -q

Failure:
...

Explain the failure first. Do not rewrite the entire solution unless necessary.
```

## Timing review

```text
M7 planned: 35 min
M7 actual: 62 min

Most time was spent understanding pytest fixtures vs mocks.

Should I revise that before M8?
```

---

# What finished means

Success is not memorizing Python syntax.

At the end, you should be able to enter an unfamiliar repository and identify:

```text
entry point
API boundary
request/response models
business/service layer
domain model
ports/contracts
infrastructure adapters
configuration
logging
database boundary
external HTTP boundary
tests
packaging/build
deployment/CI
```

Then trace one request from entry point to infrastructure and back.
