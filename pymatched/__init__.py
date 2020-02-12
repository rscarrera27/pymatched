from inspect import signature
from typing import Mapping, Any, Callable

class match:
    def __init__(self, func: Callable, *args: Any):
        try:
            self.v = func(*args)
        except Exception as e:
            self.v = e

    def __rshift__(self, cases: Mapping[Any, Callable]) -> Any:
        f = cases.get(self.v) or cases.get(type(self.v))
        if f:
            if tuple(signature(f).parameters.keys()) == ():
                return f()
            return f(self.v)

        default = cases.get(...)

        if default:
            if tuple(signature(default).parameters.keys()) == ():
                return default()
            return default(self.v)


if __name__ == "__main__":
    def fx(x):
        # raise Exception("EXcepted")
        return x

    x = match(fx, 3) >> {
        int: lambda _: int,
        str: lambda _: str,
        Exception: lambda x: print(x),
        ...: lambda: print("default")
    }
    print(f"type of x == {type(x)}")
