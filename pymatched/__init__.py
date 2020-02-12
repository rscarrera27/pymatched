from inspect import signature
from typing import Mapping, Any, Callable, Union


class pattern:
    def __init__(self, *args):
        self.possible = tuple(args)

    def __eq__(self, other):
        return other in self.possible

    def __contains__(self, item):
        return item in self.possible

    def __hash__(self):
        return hash(self.possible)


class match:
    def __init__(self, func: Union[Callable, Any], *args: Any):
        if callable(func):
            try:
                self.v = func(*args)
            except Exception as e:
                self.v = e
        else:
            self.v = func

    def __rshift__(self, cases: Mapping[Any, Callable]) -> Any:
        # pattern matching
        for p, f in cases.items():
            if type(p) == pattern and self.v in p:
                if tuple(signature(f).parameters.keys()) == ():
                    return f()
                return f(self.v)

        # basic matching
        f = cases.get(self.v) or cases.get(type(self.v))

        if f:
            if tuple(signature(f).parameters.keys()) == ():
                return f()
            return f(self.v)

        # handling default
        default = cases.get(...)

        if default:
            if tuple(signature(default).parameters.keys()) == ():
                return default()
            return default(self.v)

        raise RuntimeError("match must handle every cases.")
