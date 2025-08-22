import inspect as ins
from collections import namedtuple
from typing import *

__all__ = ["Norming"]

OPTS: tuple = ("__doc__", "__module__")
OBLS: tuple = ("__name__", "__qualname__")
BaseNorming = namedtuple("BaseNorming", ["args", "kwargs"])


class Norming(BaseNorming):
    "This class helps to create normed classes."

    def __new__(cls: type, /, *args: Any, **kwargs: Any) -> None:
        "This magic method returns a new instance."
        return BaseNorming.__new__(cls, args=args, kwargs=kwargs)

    def __call__(self: Self, norm: Callable) -> type:
        "This magic method implements calling the current instance."
        Ans: type = getclass(norm, *self.args, **self.kwargs)
        x: str
        y: Any
        for x in OPTS:
            y = getattr(norm, x)
            y = str(y)
            setattr(Ans, x, y)
        for x in OBLS:
            y = getattr(norm, x, None)
            if y is not None:
                y = str(y)
            setattr(Ans, x, y)
        sig: ins.Signature = getsignature(norm)
        Ans.__new__.__signature__ = sig
        Ans.__new__.__annotations__ = getannotations(sig)
        return Ans


def genericfunction(*args: Any, **kwargs: Any) -> Any: ...


def getannotations(sig: ins.Signature, /) -> dict:
    "This function returns an annotations dict for the __new__ magic method."
    ans: dict = dict()
    p: ins.Parameter
    for p in sig.parameters.values():
        ans[p.name] = p.annotation
    ans["return"] = sig.return_annotation
    return ans


def getclass(norm: Callable, /, *_args: Any, **_kwargs: Any) -> type:
    "This function creates a class using a given base and a given norm."

    class Ans(*_args, **_kwargs):
        "This class will be returned after overwriting this current doc string."

        def __new__(cls: type, /, *args: Any, **kwargs: Any) -> Self:
            "This magic method returns a new instance of the class."
            data: Any = norm(cls, *args, **kwargs)
            obj: Self = super().__new__(cls, data)
            return obj

    return Ans


def getsignature(norm: Callable) -> ins.Signature:
    "This function returns a signature for the __new__ magic method."
    try:
        ans: ins.Signature = ins.signature(norm)
    except ValueError:
        ans: ins.Signature = ins.signature(genericfunction)
        return ans
    params: list = list()
    p: ins.Parameter
    q: ins.Parameter
    for p in ans.parameters.values():
        if p.annotation is ins.Parameter.empty:
            q = p.replace(annotation=Any)
        else:
            q = p
        params.append(q)
    ans: ins.Signature = ins.Signature(
        parameters=params,
        return_annotation=Self,
    )
    return ans
