# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install in dev mode (includes pytest and assertpy)
pip install -e ".[dev]"

# Run all tests
pytest

# Run a single test file
pytest tests/unit/domain/test_entity.py

# Run a single test by name
pytest tests/unit/domain/test_entity.py::test_two_entities_are_equal_by_their_ids_even_with_different_properties

# Build the package (wheel + sdist → dist/)
pip install build && python -m build
```

## Architecture

This is a Python library (`dddx` on PyPI, importable as `ddd`) providing DDD building blocks as abstract base classes. The source lives under `ddd/`, tests under `tests/unit/`.

**Layer structure mirrors DDD:**

- `ddd/domain/` — Core abstractions: `ValueObject`, `Entity`, `AggregateRoot`, `DomainEvent`, plus `Identity` value object and abstract `Clock`/`EntityRepository` service interfaces.
- `ddd/application/` — `Command` and `CommandHandler` base classes.
- `ddd/infrastructure/` — `SystemClock`: the concrete UTC clock implementation.
- `ddd/test_double/` — `StubClock` and `SpyEntityRepository` shipped as part of the library for consumers to use in their own tests.

**Key design patterns:**

- `ValueObject`, `Command`, and `CommandHandler` inherit from `Immutable` (from the `underpyx` dependency), so attributes are frozen after `__init__`. Attempting to mutate them raises `AttributeError`.
- `Entity` equality is by `id`; `ValueObject` equality compares all `__dict__` values.
- `AggregateRoot` uses the protected `_record_that(event)` method (called internally by domain methods) and the public `release_events()` to atomically drain the event list. Calling `release_events()` twice returns an empty list the second time.
- `EntityRepository.get()` wraps the abstract `find()` and raises typed `EntityNotFound` (a `RuntimeError` subclass) when not found. Subclasses only implement `find()` and `save()`.
- `Identity` wraps UUIDs: generate with `Identity.new()`, parse from string with `Identity.from_string(...)`.
- Constructor parameters for entity/aggregate IDs use `id_` (trailing underscore) to avoid shadowing Python's built-in `id`.

**Test conventions:**

- Tests use `assertpy`'s `assert_that(...).is_equal_to(...)` style alongside `pytest.raises`.
- AAA pattern (arrange / act / assert) is made explicit with inline comments.
- Test function names are fully descriptive snake_case sentences.
