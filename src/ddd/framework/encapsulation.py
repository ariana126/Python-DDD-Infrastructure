import inspect
from abc import ABC

# TODO: Make _check_ functions and _initialized private.

class Encapsulated(ABC):
    def __getattribute__(self, name):
        # Skip internal attributes and methods to avoid recursion
        if (name.startswith('_Encapsulated__') or
                name.startswith('_check_') or
                name in ('_initialized', '__dict__', '__class__')):
            return object.__getattribute__(self, name)

        # Handle encapsulation
        if name.startswith('__') and not name.endswith('__'):
            # Private attribute
            if not self._check_private_access(name):
                raise AttributeError(f"Cannot access private attribute {name}")
        elif name.startswith('_') and not name.startswith('__'):
            # Protected attribute
            if not self._check_protected_access(name):
                raise AttributeError(f"Cannot access protected attribute {name}")

        return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        # Handle encapsulation checks first
        if hasattr(self, '_initialized'):  # Only check after initialization
            if name.startswith('__') and not name.endswith('__'):
                # Private attribute - check access
                if not self._check_private_access(name):
                    raise AttributeError(f"Cannot access private attribute {name}")
            elif name.startswith('_') and not name.startswith('__'):
                # Protected attribute - check access
                if not self._check_protected_access(name):
                    raise AttributeError(f"Cannot access protected attribute {name}")

        # Call parent's __setattr__ (cooperative inheritance)
        super().__setattr__(name, value)

    def _check_private_access(self, name):
        """Check if private attribute access is allowed"""
        try:
            frame = inspect.currentframe().f_back.f_back
            caller_locals = frame.f_locals
            caller_class = None

            if 'self' in caller_locals:
                caller_class = caller_locals['self'].__class__
            elif 'cls' in caller_locals:
                caller_class = caller_locals['cls']

            # Private access only allowed from exact same class
            return caller_class is self.__class__
        except:
            return False

    def _check_protected_access(self, name):
        """Check if protected attribute access is allowed"""
        try:
            frame = inspect.currentframe().f_back.f_back
            caller_locals = frame.f_locals
            caller_class = None

            if 'self' in caller_locals:
                caller_class = caller_locals['self'].__class__
            elif 'cls' in caller_locals:
                caller_class = caller_locals['cls']

            # Protected access allowed from same class or subclasses
            return (caller_class is self.__class__ or
                    (caller_class and issubclass(caller_class, self.__class__)) or
                    (caller_class and issubclass(self.__class__, caller_class)))
        except:
            return False