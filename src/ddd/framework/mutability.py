from abc import ABC, ABCMeta

# TODO: Make _initialized private.

class ImmutableMeta(ABCMeta):
    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        instance._initialized = True
        return instance

class Immutable(ABC, metaclass=ImmutableMeta):
    def __setattr__(self, name, value):
        if hasattr(self, '_initialized'):
            raise AttributeError(f"Cannot modify immutable object")
        super().__setattr__(name, value)

    def __delattr__(self, name):
        if hasattr(self, '_initialized'):
            raise AttributeError(f"Cannot delete from immutable object")
        super().__delattr__(name)