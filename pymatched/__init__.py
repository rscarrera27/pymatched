import types
from inspect import signature
from typing import Mapping, Any, Callable, Union
from uuid import uuid4


def do(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return e


class PlaceholderType:
    def __hash__(self):
        return hash(uuid4().hex)

    def __eq__(self, other):
        return True


_ = PlaceholderType()


class oneof:
    def __init__(self, *args):
        self.possibles = tuple(args)

    def __eq__(self, other):
        return other in self.possibles

    def __contains__(self, item):
        return item in self.possibles

    def __hash__(self):
        return hash(uuid4().hex)


class match:
    def __init__(self, target: Union[Callable, Any], *args: Any):
        self.target = target

    def __rshift__(self, cases: Mapping[Any, Any]) -> Any:
        # if this is nested match
        if (self.target is Ellipsis) or (self.target is _):
            return lambda p: match(p) >> cases

        # 1st order

        try:
            actn = cases.get(self.target)  # exact value match
        except TypeError:  # raised when try to get with unhashable data
            pass
        else:
            if actn:
                return self._do(actn)

        # 2nd order
        for ptrn, actn in cases.items():
            if self._match_oneof(ptrn):  # a | b | c => action
                return self._do(actn)
            if self._match_placeholder(ptrn):  # (a, _, c) => action
                return self._do(actn)
            if self._match_type_with_guard(ptrn):  # (<type>, <lambda x -> bool>) => action
                return self._do(actn)
        # 3rd order
        actn = cases.get(type(self.target))  # <type> => action
        if actn:
            return self._do(actn)

        # handling default
        default = cases.get(Ellipsis) or cases.get(Any)

        if default:
            return self._do(default)

        raise RuntimeError("match must handle every cases.")

    def _do(self, case):
        if callable(case):
            if tuple(signature(case).parameters.keys()) == ():
                return case()
            return case(self.target)
        elif isinstance(case, tuple) or isinstance(case, list):
            if len(case) >= 1 and callable(case[0]):
                f = case[0]
                args = (arg for arg in case[1:] if arg != _)
                if _ in case:
                    return f(self.target, *args)
                else:
                    return f(*args)
        else:
            return case

    def _match_oneof(self, ptrn) -> bool:
        is_match = False

        if isinstance(ptrn, oneof) and (self.target in ptrn):
            is_match = True

        return is_match

    def _match_placeholder(self, ptrn) -> bool:
        return self.target == ptrn

    # def _match_wildcard(self, ptrn, target):
    #     if (not ptrn) and (not target):
    #         return True
    #
    #     if (len(ptrn) > 1) and ptrn[0] == Ellipsis and (not target):
    #         return False
    #
    #     if ((len(ptrn) > 1) and ptrn[0] == _) or (ptrn and target and ptrn[0] == target[0]):
    #         return self._match_wildcard(ptrn[1:], target[1:])
    #
    #     if len(ptrn) != 0 and ptrn[0] == Ellipsis:
    #         return self._match_wildcard(ptrn[1:], target) or self._match_wildcard(ptrn, target[1:])
    #
    #     return False

    def _match_type_with_guard(self, ptrn) -> bool:
        is_match = False

        if isinstance(ptrn, tuple) and len(ptrn) ==2:
            t = ptrn[0]
            guard = ptrn[1]
            if type(self.target) == t and isinstance(guard, types.LambdaType) and guard(self.target):
                is_match = True

        return is_match
