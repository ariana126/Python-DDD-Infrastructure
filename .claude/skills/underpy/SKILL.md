---
name: underpy
description: >
  Teaches agents how to use the underpy package (PyPI: underpyx) — a pure-Python utility library
  providing strict OOP guarantees via abstract base classes. Use when writing code that imports
  underpy, uses Encapsulated, Immutable, ServiceClass, JSON, or Fn, or when the user asks about
  enforcing access control, immutability, encapsulation, private/protected attributes, callable
  wrappers, or JSON type hints in Python.
---

## Overview

`underpy` (installed as `underpyx`) is a zero-dependency Python library providing abstract base
classes (ABCs) that enforce strict OOP guarantees — real access control and immutability — which
Python does not enforce natively.

```bash
pip install underpyx
```

Five names are exported from `underpy`:

| Export | Kind | Purpose |
|---|---|---|
| `Encapsulated` | ABC | Enforces `_protected` / `__private` access at runtime |
| `Immutable` | ABC | Freezes all attributes after `__init__` completes |
| `ServiceClass` | ABC | Composite of `Encapsulated + Immutable + ABC` |
| `JSON` | Type alias | Recursive type hint for arbitrary JSON-structured data |
| `Fn` | Concrete class | Immutable, encapsulated callable wrapper |

---

## `Encapsulated` — runtime access control

Subclass `Encapsulated` to get enforced `_protected` / `__private` semantics via
`inspect.currentframe()` stack inspection.

```python
from underpy import Encapsulated

class BankAccount(Encapsulated):
    def __init__(self, owner: str, balance: float):
        self.owner = owner          # public — accessible anywhere
        self._ledger = []           # protected — only this class and subclasses
        self.__pin = "1234"         # private — only this exact class

    def deposit(self, amount: float) -> None:
        self._ledger.append(amount)   # ✅ protected access inside the class

    def _audit(self) -> list:         # protected method — callable by subclasses
        return self._ledger

    def __verify(self, pin: str) -> bool:  # private method — only BankAccount
        return self.__pin == pin
```

### Access-control rules

| Caller location | `public` | `_protected` | `__private` |
|---|---|---|---|
| Outside the class | ✅ | ❌ `AttributeError` | ❌ `AttributeError` |
| Same class methods | ✅ | ✅ | ✅ |
| Subclass methods | ✅ | ✅ | ❌ `AttributeError` |

```python
account = BankAccount("Alice", 0)
account.owner               # ✅ "Alice"
account._ledger             # ❌ AttributeError: Cannot access protected attribute _ledger
account.__pin               # ❌ AttributeError (also name-mangled by Python)

class SavingsAccount(BankAccount):
    def get_ledger(self):
        return self._ledger   # ✅ protected access is allowed in subclasses
    def get_pin(self):
        return self.__pin     # ❌ AttributeError: private is off-limits to subclasses
```

### Key implementation note

- `Encapsulated` is an `ABC` — it **cannot** be instantiated directly.
- Access is checked on both reads (`__getattribute__`) and writes (`__setattr__`).
- Inside `__init__`, writes are unrestricted (the `_initialized` guard is not yet set).

---

## `Immutable` — freeze after `__init__`

Subclass `Immutable` to make all instance attributes read-only after construction.

```python
from underpy import Immutable

class Config(Immutable):
    def __init__(self, host: str, port: int):
        self.host = host    # ✅ set freely inside __init__
        self.port = port    # ✅

cfg = Config("localhost", 8080)
cfg.port = 9000             # ❌ AttributeError: Cannot modify immutable object
del cfg.host                # ❌ AttributeError: Cannot delete from immutable object
cfg.timeout = 30            # ❌ AttributeError: Cannot modify immutable object
```

### How it works

`Immutable` uses `ImmutableMeta` (a metaclass extending `ABCMeta`). After `__init__` returns, the
metaclass stamps `_initialized = True` on the instance. From then on, `__setattr__` and
`__delattr__` always raise `AttributeError`.

- `Immutable` is an `ABC` — must be subclassed.
- Attributes may only be set inside `__init__`.

---

## `ServiceClass` — service-layer base

`ServiceClass` is a three-line composite of `Encapsulated + Immutable + ABC`. Use it as the base
class for service objects that must be both immutable and have enforced access control.

```python
from underpy import ServiceClass

class EmailService(ServiceClass):
    def __init__(self, smtp_host: str, api_key: str):
        self._smtp_host = smtp_host   # protected
        self.__api_key = api_key      # private

    def send(self, to: str, body: str) -> bool:
        # can access self._smtp_host and self.__api_key here
        return True

svc = EmailService("smtp.example.com", "secret")
svc.send("user@example.com", "Hello")  # ✅
svc._smtp_host                         # ❌ AttributeError (protected)
svc._smtp_host = "other"               # ❌ AttributeError (immutable + protected)
```

Both constraint systems — access control and immutability — apply simultaneously because
`Encapsulated.__setattr__` and `Immutable.__setattr__` chain via `super()`.

---

## `JSON` — recursive JSON type alias

`JSON` is a `typing.Union` type alias covering every valid JSON value. Use it in annotations
wherever a function accepts or returns arbitrary JSON-structured data.

```python
from underpy import JSON
from typing import Dict

def parse_api_response(data: JSON) -> str:
    if isinstance(data, dict):
        return data.get("message", "")
    return str(data)

def build_payload(name: str, value: int) -> Dict[str, JSON]:
    return {"name": name, "value": value, "meta": None}
```

`JSON` expands to:
```
str | int | float | bool | None | Dict[str, JSON] | List[JSON]
```

It is a pure type-checking alias — zero runtime overhead, no ABCs or classes involved.

---

## `Fn` — immutable callable wrapper

`Fn` wraps a callable with its arguments into an immutable, encapsulated object. It inherits both
`Encapsulated` and `Immutable`, so the wrapped callback cannot be changed after construction.

```python
from underpy import Fn

# Wrap a plain function with pre-bound arguments
def greet(name: str) -> str:
    return f"Hello, {name}"

fn = Fn(greet, "Alice")
fn.call()                   # ✅ "Hello, Alice"
fn.is_function(greet)       # ✅ True
```

### Wrapping bound methods

```python
class Notifier:
    def __init__(self, channel: str):
        self._channel = channel

    def notify(self, msg: str) -> str:
        return f"[{self._channel}] {msg}"

n1 = Notifier("slack")
n2 = Notifier("email")

fn = Fn(n1.notify, "Deploy complete")
fn.call()                    # ✅ "[slack] Deploy complete"
fn.is_function(n1.notify)    # ✅ True — same method on same instance
fn.is_function(n2.notify)    # ✅ False — same method name, different instance
```

### Constructor signature

```python
Fn(callback, *args, **kwargs)
```

- `callback` — any callable (function, lambda, bound method)
- `*args` / `**kwargs` — positional and keyword arguments bound to the call

### Methods

| Method | Signature | Returns | Description |
|---|---|---|---|
| `call` | `call() -> R` | return value of wrapped callable | Invokes callback with bound args |
| `is_function` | `is_function(fn) -> bool` | `bool` | Identity check; handles bound methods correctly |

### `is_function` identity semantics

- **Plain functions**: uses `is` identity — two references to the same function object compare as `True`.
- **Bound methods**: compares both `__func__` (underlying function) **and** `__self__` (bound instance), so the same method on two different instances compares as `False`.

---

## Combining the ABCs

The ABCs compose naturally via standard Python MRO:

```python
from underpy import Encapsulated, Immutable

class Token(Encapsulated, Immutable):
    def __init__(self, value: str, scopes: list):
        self._value = value       # protected + immutable
        self.__scopes = scopes    # private + immutable

    def has_scope(self, scope: str) -> bool:
        return scope in self.__scopes  # ✅ private access inside class

token = Token("abc123", ["read", "write"])
token.has_scope("read")   # ✅ True
token._value              # ❌ AttributeError (protected)
token._value = "x"        # ❌ AttributeError (immutable + protected)
```

---

## Common errors and fixes

| Error | Cause | Fix |
|---|---|---|
| `AttributeError: Cannot access protected attribute _x` | Accessing `_x` from outside the class hierarchy | Only access protected attributes inside the class or its subclasses |
| `AttributeError: Cannot modify immutable object` | Setting an attribute after `__init__` on an `Immutable` subclass | Set all values inside `__init__`; treat the object as read-only after construction |
| `TypeError: Can't instantiate abstract class X` | Instantiating `Encapsulated`, `Immutable`, or `ServiceClass` directly | These are ABCs — always subclass them first |
| `Fn` wraps wrong arguments | Passing args at `call()` time instead of construction time | Pass all arguments to `Fn(callback, *args, **kwargs)` at construction |

---

## Installation and import

```bash
# Install
pip install underpyx

# Import
from underpy import Encapsulated, Immutable, ServiceClass, JSON, Fn

# Or selectively
from underpy import Encapsulated
from underpy import JSON
```

- PyPI package name: **`underpyx`**
- Python import name: **`underpy`**
- Requires Python **≥ 3.10** (uses `ParamSpec`)
- Zero runtime dependencies
