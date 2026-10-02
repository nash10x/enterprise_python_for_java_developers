from collections.abc import Iterator
from contextlib import contextmanager


@contextmanager
def transaction(name: str) -> Iterator[None]:
    print(f"[TX] BEGIN {name}")
    try:
        yield
        print(f"[TX] COMMIT {name}")
    except Exception:
        print(f"[TX] ROLLBACK {name}")
        raise
