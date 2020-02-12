<h1 align="center">⏩ pymatched ⏩</h1>

# What is pymatched?
pymatched is a library which provides functional pattern matching.

# Installation
```bash
pip install pymatched
```

# Syntax
```python
result = match([<'func or func result'>], <'func args if needed'>) >> Mapping[Case, Callable]
```

## Match order
pattern >> value >> type >> default(if defined)

# Usage

## Value match

```python
from pymatched import match

fx = lambda x: x

match(fx(5)) >> {
    1: lambda: print("catch 1"),
    5: lambda: print("catch 5"),
}
```

## Type match
```python
from pymatched import match

fx = lambda x: x

match(fx(5)) >> {
    str: lambda: print("catch str"),
    int: lambda: print("catch int"),
}
```

### Exception match in type match
```python
from pymatched import match

def fx(v):
    raise Exception("Ooops!")

match(fx, 5) >> {
    Exception: lambda e: print(e),
    int: lambda: print("catch int"),
}
```

## Pattern match
```python
from pymatched import pattern, match

fx = lambda x: x

match(fx(5)) >> {
    pattern(*[i for i in range(0, 10)]): lambda: print("pattern 1"),  # 1 ... 10 => print('pattern 1')
    pattern(*[i for i in range(10, 20)]): lambda: print("pattern 2"),  # 11 ... 20 => print('pattern 2')
}
```

## Handling default case
use elipsis (...).

if nothing catched but default handler not defined, RuntimeError will be raised.

```python
from pymatched import match

fx = lambda x: x

match(fx(5)) >> {
    ...: lambda: print("default"),
}
```

## Nested match

```python
from pymatched import match

fx = lambda x: x

match(fx(5)) >> {
    int: lambda i: match(i) >> {
        5: lambda: print("it's five")
    },
}
```

## Mixed match
```python
from pymatched import pattern, match

v = fx(14)

# x = match(fx, 14) >> {
x = match(v) >> {
    int: lambda v: print(f"{v} is int"),
    str: lambda v: print(f"{v} is str"),
    pattern(*[i for i in range(0, 10)]): lambda x: print("pattern 1 catched"),
    pattern(*[i for i in range(10, 20)]): lambda x: print("pattern 2 catched"),
    Exception: lambda x: print(x),
    ...: lambda: print("default")
}
```
