*<h1 align="center">py<b>matched⇒</b></h1>*

# 🤖 What is pymatched?
pymatched is a library which provides functional pattern matching.

# ⚡️Installation
```bash
pip install pymatched
```

# ⏩ Syntax
```python
result = match('func') >> {
    Case: Action
}
```

- `Action` could be a data or callable(takes one or no argument)
- If `Action` is callable and takes one argument, match pass matched value as parameter.
- If `Action` is simple data, match just return it

## 📖 Match order
1. exact match
2. oneof match
3. placeholder match (if target is immutable iterable)
4. type match with guard (Contravariant match)
5. type match (Invariant match)
6. type match (Contravariant match)
7. handling default if exists

# 🏃‍♀️ Usage

### **⚠️ match mutables**
as you know, mutable things cannot be key of dict so we can not match easly.

this is the example of list.

#### Case A: use type guards

```python
from pymatched import oneof, match

x = match([1, 2, 3]) >> {
    list                            : "list",
    oneof([1], [1, 2], [1, 2, 3])   : "[1] | [1, 2] | [1, 2, 3]",
    (list, lambda x: x == [1, 2, 3]): "(list, f(list) -> bool)",
    # [1, 2, 3]: "[1, 2, 3]",  --> list is unhashable so not working
}
```

#### Case B: use nested match

```python
from pymatched import match, _

x = match([1, 2, 3]) >> {
    list: match(...) >> {
        (list, lambda v: v == [1, _, 3]): "pattern is (1, * ,3)",
        ...                             : "default"
    } 
}
```


## Value match

```python
from pymatched import match

match(1) >> {
    1: "It's 1",
    5: "It's 5",
}
```

## Handling default case
use elipsis `...` or `typing.Any`

if nothing catched but default handler not defined, RuntimeError will be raised.

```python
from typing import Any
from pymatched import match

match(None) >> {
    ...: "default",
    # Any: "also default",
}
```

## Type match
```python
from pymatched import match

match(42) >> {
    int: "int caught",
    ...: lambda v: f"{type(v)} caught"
}
```

###  Type match with guard

If tuple's first element is type and second element is lambda, this case will be considered as type match with guard.

```python
from pymatched import match

match(42) >> {
    (int, lambda v: v == 42): "42 caught",
    int                      : "int except 42",
}
```

type match with guard can use `typing.Any`.

```python
from typing import Any
from pymatched import match

match(42) >> {
    (Any, lambda v: v in (42, "42")): "42 caught",
    int                              : "int except 42",
}
```

### Exception match in type match

`pymatched.do` wraps executing function. when wrapped function raises error, `do` catch it and return it as normal return. 

```python
from pymatched import match, do

def fx(v):
    raise Exception("Ooops!")

match(do(fx, None)) >> {
    Exception: "exception caught",
    ...      : lambda v: f"{v} caught",
}
```

## OneOf match
```python
from pymatched import oneof, match

fx = lambda x: x

match(fx(5)) >> {
    oneof(1, 2, 3): "one of 1, 2, 3",
    oneof(4, 5, 6): "one of 4, 5, 6",
}
```

## Placeholder match

```python
from pymatched import match, _

match((1, 2, 3, 4)) >> {  # change (1, 2, 3, 4) into (100, 2, 3, 4) or (1, 9, 3, 9)
    (1, _, 3, _): "pattern (1, *, 3, *)",
    (_, 2, _, 4): "pattern (*, 2, *, 4)",
}
```

## Nested match

If match with `pymatchied._` (PlaceholderTyoe) or `...` (Ellipsis), this match will be considered as nested match.

```python
from pymatched import match, _

match(5) >> {
    int: match(_) >> {
        5: "It's 5",
        ...: "default"
    },
}
```

## Mixed match

cases could be mixed, but resolved by designated match order.

```python
from pymatched import oneof, match, _

v = (1, 2, 3)

x = match(v) >> {
    tuple                         : "Tuple caught",
    (tuple, lambda v: v[-1] == 3) : "last item of tuple is 3",
    (1, _, 3)                     : "pattern is (1, *, 3)",
    oneof((1,), (1, 2), (1, 2, 3)): "one of (1,) | (1, 2) | (1, 2, 3)",
    (1, 2, 3)                     : "(1, 2, 3)",
}
```
