# Python-DDD-Infrastructure

**A lightweight Python package for implementing Domain-Driven Design (DDD) building blocks.**  
Provides base classes for `ValueObject`, `Entity`, `AggregateRoot`, and `DomainEvent`, plus utility mixins for immutability and encapsulation.

---

## ✨ Features

- 📦 **Core DDD Building Blocks**
  - `ValueObject` — immutable, equality-by-value objects.
  - `Entity` — objects identified by unique ID.
  - `AggregateRoot` — transactional consistency boundary.
  - `DomainEvent` — base class for event-sourced or message-driven domains.

- 🔒 **Utility Foundations**
  - `Immutable` base — automatic immutability enforcement.
  - `Encapsulated` base — protected internal state with controlled exposure.
---

## 📦 Installation

Clone the repository and install it locally:

```bash
git clone https://github.com/ariana126/Python-DDD-Infrastructure.git
cd Python-DDD-Infrastructure
pip install -e .[test]
```

Or set it in your `requirements.txt` as 
`git+https://github.com/ariana126/Python-DDD-Infrastructure.git@main#egg=ddd`
