# Python‑DDD‑Infrastructure

**A lightweight Python library offering building blocks for Domain‑Driven Design (DDD).**
Provides base classes and utility mixins to help structure your domain model cleanly in terms of entities, value objects, aggregates, and events.

---

## ✨ Features

* **Core DDD abstractions:**

  * `ValueObject` — immutable objects compared by value.
  * `Entity` — objects with a unique identity.
  * `AggregateRoot` — consistency boundary for aggregates.
  * `DomainEvent` — support for domain events in an event‑driven or event‑sourced architecture.

* Clean, minimal dependencies and a small surface area so you can integrate it with your existing projects without a heavy footprint.

---

## 📦 Installation

Install from source:

```bash
pip install git+https://github.com/ariana126/Python‑DDD‑Infrastructure.git
```
or PyPI
```bash
pip install dddx
```

---

## 🛠 Usage

Here’s a simple example of how you might use the components in your domain layer.

```python
from ddd import ValueObject, Entity, AggregateRoot, DomainEvent

# Value Object Example
class Money(ValueObject):
    def __init__(self, amount: float, currency: str):
        self._amount = amount
        self._currency = currency

    @property
    def amount(self):
        return self._amount

    @property
    def currency(self):
        return self._currency

# Entity Example
class Product(Entity):
    def __init__(self, product_id: str, name: str, price: Money):
        super().__init__(entity_id=product_id)
        self._name = name
        self._price = price

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

# AggregateRoot + DomainEvent Example
class ProductCreated(DomainEvent):
    def __init__(self, product_id: str, name: str, price: Money):
        self.product_id = product_id
        self.name = name
        self.price = price

class Inventory(AggregateRoot):
    def __init__(self, inventory_id: str):
        super().__init__(aggregate_id=inventory_id)
        self._products = {}

    def add_product(self, product: Product):
        # Some business invariants could be checked here
        self._products[product.id] = product
        self.record_event(ProductCreated(product.id, product.name, product.price))
```

---

## ✅ Testing

This project uses `pytest` for unit tests.

To run tests:

```bash
pytest
```

---

## 🌐 Contribution

Contributions are very welcome! If you find bugs, have ideas for enhancements, or want to add features, please feel free to open an issue or a pull request. Some suggestions:

* Add more domain values (e.g. price, currency)
* Support serialization / deserialization of aggregates and events
* Expand documentation, provide practical real‑world examples

---

## 📄 License

This project is released under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Acknowledgments

Thanks to anyone who has contributed or will contribute. Built for folks who want to work cleanly with DDD in Python, without getting locked into large frameworks.

---

*Built with care by the community, for domain experts and software designers.*
