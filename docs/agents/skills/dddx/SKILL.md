---
name: dddx
description: >
    Teaches agents how to use the dddx package (PyPI: dddx, importable as `ddd`) — a Python library of Domain-Driven Design building blocks. Use when writing code that imports `ddd`, subclasses ValueObject, Entity, AggregateRoot, DomainEvent, EntityRepository, Clock, Command, or CommandHandler, or when the user asks to model a domain using DDD patterns in Python.
---

## Overview

`dddx` provides abstract base classes for Domain-Driven Design (DDD) in Python. Import from the top-level `ddd` package:

```python
from ddd import ValueObject, Entity, AggregateRoot, DomainEvent
from ddd import Identity, Clock, EntityRepository
from ddd.application import Command, CommandHandler
from ddd.infrastructure import SystemClock
from ddd.test_double import StubClock, SpyEntityRepository
```

**Key constraint:** `ValueObject`, `Command`, and `CommandHandler` inherit from `underpy.Immutable` — all attributes are **frozen after `__init__`**. Attempting to set, delete, or add attributes afterward raises `AttributeError`.

---

## Class Reference

### `Identity(ValueObject)`

Wraps a UUID string. Always use `Identity` for entity/aggregate IDs — never raw strings.

```python
id_ = Identity.new()                    # generate a fresh UUID4
id_ = Identity.from_string("some-id")  # wrap an existing string
str(id_)                                # "some-id"
id_.as_string                           # "some-id"
```

Two `Identity` objects with the same string are equal (`==`) and share the same hash.

---

### `ValueObject(Immutable, ABC)`

Equality is by **value** (all attributes compared by sorted name, recursively for nested `ValueObject`s).

```python
class Money(ValueObject):
    def __init__(self, amount: float, currency: str):
        self._amount = amount      # use protected or private attrs
        self._currency = currency

    @property
    def amount(self): return self._amount

    @property
    def currency(self): return self._currency

m1 = Money(10.0, "USD")
m2 = Money(10.0, "USD")
m1 == m2          # True
m1.amount = 5.0   # raises AttributeError — immutable!
```

---

### `Entity(ABC)`

Equality is by **identity** (`id` property), not attributes. Constructor parameter is always `id_` (trailing underscore to avoid shadowing `id`).

```python
class Product(Entity):
    def __init__(self, id_: Identity, name: str):
        self._name = name
        super().__init__(id_)   # call super AFTER setting own attrs

    @property
    def name(self): return self._name
```

- `entity.id` → the `Identity` object
- Two entities with the same `id_` are equal even if other attributes differ.
- `Entity` is **not hashable** (no `__hash__`).

---

### `AggregateRoot(Entity, ABC)`

Extends `Entity` with a domain-event accumulator.

```python
class OrderPlaced(DomainEvent):
    def __init__(self, order_id: str): self.order_id = order_id

class Order(AggregateRoot):
    def __init__(self, id_: Identity):
        super().__init__(id_)
        self._items = []

    def place(self):
        # business logic …
        self._record_that(OrderPlaced(self.id.as_string))   # protected

events = order.release_events()   # drains the list (single-release guarantee)
order.release_events()            # returns [] — already drained
```

- **`_record_that(event)`** — protected; call inside domain methods only.
- **`release_events()`** — public; atomically drains and returns the event list.

---

### `DomainEvent(ABC)`

Pure abstract marker. Subclass it and add whatever attributes the event needs.

```python
class UserRegistered(DomainEvent):
    def __init__(self, user_id: str, email: str):
        self.user_id = user_id
        self.email = email
```

---

### `EntityRepository(ABC)`

Implement `find` and `save`; `get` is provided and raises `EntityNotFound` automatically.

```python
from ddd import EntityRepository, Identity, AggregateRoot
from ddd.domain.service import EntityNotFound

class OrderRepository(EntityRepository):
    def __init__(self):
        self._store: dict[str, Order] = {}

    def find(self, _id: Identity) -> Order | None:
        return self._store.get(_id.as_string)

    def save(self, entity: Order) -> None:
        self._store[entity.id.as_string] = entity

# Usage
repo = OrderRepository()
order = repo.get(some_id)       # raises EntityNotFound if absent
order = repo.find(some_id)      # returns None if absent
```

`EntityNotFound` is a `RuntimeError` subclass with a `with_id(_id)` static factory.

---

### `Clock(ABC)` / `SystemClock`

```python
from ddd import Clock
from ddd.infrastructure import SystemClock
from datetime import datetime

class MyService:
    def __init__(self, clock: Clock):
        self._clock = clock

    def timestamp(self) -> datetime:
        return self._clock.now()

service = MyService(SystemClock())   # production
```

`SystemClock.now()` returns `datetime.now(timezone.utc)` — always UTC-aware.

---

### `Command` / `CommandHandler`

Both inherit `Immutable` — commands are frozen DTOs; handlers are frozen after construction.

```python
from ddd.application import Command, CommandHandler

class RegisterUser(Command):
    def __init__(self, email: str, name: str):
        self.email = email
        self.name = name

class RegisterUserHandler(CommandHandler):
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def handle(self, command: RegisterUser) -> None:
        user = User.register(Identity.new(), command.email, command.name)
        self.repo.save(user)
```

---

## Test Doubles

The library ships ready-made test doubles — import them in your own test suite.

### `StubClock`

```python
from ddd.test_double import StubClock
from datetime import datetime, timezone

fixed_time = datetime(2024, 1, 1, tzinfo=timezone.utc)
clock = StubClock(fixed_time)
clock.now()   # always returns fixed_time
```

### `SpyEntityRepository`

In-memory repository with a built-in `assertpy` assertion helper.

```python
from ddd.test_double import SpyEntityRepository

repo = SpyEntityRepository()
repo.save(my_aggregate)
found = repo.find(my_aggregate.id)     # returns the aggregate
repo.assert_database_is_empty()        # fails test if any entities are stored
```

`get(_id)` raises `EntityNotFound` if the entity was not previously `save`d.

---

## Patterns & Conventions

- **`id_` parameter name** — all entity/aggregate constructors accept `id_` (trailing underscore) to avoid shadowing the built-in `id`.
- **`super().__init__(id_)` placement** — call `super().__init__` *after* setting your own attributes in entity/aggregate constructors; `Immutable` freezes the object after init completes.
- **Private vs protected attributes** — use `self._attr` (protected) for attributes subclasses may need; use `self.__attr` (private/mangled) for truly internal state.
- **Event sourcing lifecycle** — call `_record_that` inside the aggregate's business methods, never from outside. Dispatch `release_events()` once (e.g. in the repository save or application service) — the list is cleared on first call.
- **ValueObject nesting** — nested `ValueObject` instances in equality comparisons are handled automatically; no extra work needed.
