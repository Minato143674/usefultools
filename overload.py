import inspect
from typing import Callable, TypeVar
from functools import update_wrapper

F = TypeVar("F", bound=Callable)
_namespace_overloads = {}

class Dispether:
    def __init__(self, func: Callable, validate_signature = False):
        self.overloads = {}
        self.validate_signature = validate_signature
        self.__signature__ = inspect.signature(func)
        self._name_func = func.__qualname__
        self.__wrapped__ = func
        self.__annotations__ = func.__annotations__
        self.__name__ = func.__name__
        self.__qualname__ = func.__qualname__
        self.__doc__ = func.__doc__

    def registry_func(self, func: Callable):
        hints = func.__annotations__
        sig = func.__code__.co_varnames[:func.__code__.co_argcount]
        signature = tuple(hints.get(name) for name in sig if name != "self" and name != "cls")
        if signature in self.overloads:
            if self.validate_signature:
                raise ValueError(f"Сигнатура {signature} уже есть!!!")
            print(f"Сигнатура {signature} уже есть!!!")

        self.overloads[signature] = func
        return self

    def __call__(self, *args, **kwargs):
        a = list(map(type, args))
        b = list(map(type, kwargs))
        c = tuple(a + b)
        fn = self.overloads.get(c)
        if fn is None:
            raise TypeError(
                f"No matching overload for '{self._name_func}' "
                f"with argument types {c}"
            )
        
        return fn(*args, **kwargs)

    def _call_with_instance(self, instance, *args, **kwargs):
        a = list(map(type, args))
        b = list(map(type, kwargs))
        c = tuple(a + b)
        fn = self.overloads.get(c)

        if fn is None:
            raise TypeError(
                f"No matching overload for '{self._name_func}' "
                f"with argument types {c}"
            )

        return fn(instance, *args, **kwargs)

    def __get__(self, instance, owner):
        if instance is None:
            return self

        def bound(*args, **kwargs):
            return self._call_with_instance(instance, *args, **kwargs)

        return bound

def overload(*, validate_signature: bool = False):
    """Декоратор для перегрузки. Для работы обязательно аннотировать параметры функции"""
    def decorator(func: F) -> F:
        name_func = func.__qualname__
        dispether: Dispether = _namespace_overloads.get(name_func)
        if dispether:
            return dispether.registry_func(func)
        else:
            dispether = Dispether(func, validate_signature)
            dispether.registry_func(func)
            _namespace_overloads[name_func] = dispether
            update_wrapper(dispether, func)
        
        return dispether
    return decorator
