from typing import Callable, Concatenate, ParamSpec, Self, TypeVar, Union

import bpy
from bpy.props import (
    BoolProperty,
    BoolVectorProperty,
    CollectionProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
    IntProperty,
    IntVectorProperty,
    PointerProperty,
    StringProperty,
)
from bpy.types import Context

"""
This is my attempt at a method of defining Blender properties while maintaining useful type hinting.
I have no idea if it's worth it, or if it's massive overkill, but it does make me feel better.

Some notes:
    - properties need to be defined using the "=" sign rather than the ":" sign
      (this is because type hints aren't propagated through function calls)
"""


# files = set()


P = ParamSpec("P")
T = TypeVar("T")
R = TypeVar("R")  # The return type of the decorated function


def override_prop_return(
    fun: Callable[P, T]
) -> Callable[[Callable[Concatenate[Callable[P, T], P], R]], Callable[P, R]]:
    """This is some type magic that lets the decorated function inherit the type signature of another function.
    It's pretty mind bending: https://github.com/python/mypy/issues/10574#issuecomment-1902246197.
    I modified it to allow you to override the return type, allowing creating wrapper functions
    that type hint a different return type to reality."""

    def decorator(wrapper: Callable[Concatenate[Callable[P, T], P], R]) -> Callable[P, R]:

        def decorated(*args: P.args, **kwargs: P.kwargs) -> T:
            # add_file()
            return fun(*args, **kwargs)

        return decorated

    return decorator


# def add_file():
#     """Add a file to the list for having BProperties converted into regular properties"""
#     files.add(inspect.stack()[2].filename)


class BProperty:

    def __init__(self, name: str):
        self._name = name

    def __repr__(self):
        return f"BProperty('{self._name}')"

    def draw(self, layout, *args, **kwargs):
        print(self._name, layout, args, kwargs)


@override_prop_return(StringProperty)
def BStringProperty(*args, **kwargs) -> Union[str, BProperty]:
    return StringProperty(*args, **kwargs)


@override_prop_return(EnumProperty)
def BEnumProperty(*args, **kwargs) -> str: ...


@override_prop_return(IntProperty)
def BIntProperty(*args, **kwargs) -> int: ...


@override_prop_return(IntVectorProperty)
def BIntVectorProperty(*args, **kwargs) -> list[int]: ...


@override_prop_return(BoolProperty)
def BBoolProperty(*args, **kwargs) -> bool:
    return BoolProperty(*args, **kwargs)


@override_prop_return(BoolVectorProperty)
def BBoolVectorProperty(*args, **kwargs) -> list[bool]: ...


@override_prop_return(FloatProperty)
def BFloatProperty(*args, **kwargs) -> float: ...


@override_prop_return(FloatVectorProperty)
def BFloatVectorProperty(*args, **kwargs) -> list[float]: ...


@override_prop_return(CollectionProperty)
def BCollectionProperty(*args, **kwargs) -> bpy.types.bpy_prop_collection: ...


# Since the PointerProperty return type hint is dependent on its input arguments,
# I implemented this one manually without using the decorator
# I can't be bothered to add a docstring for it.
def BPointerProperty(
    type: T,
    name: str = "",
    description: str = "",
    translation_context: str = "*",
    options: set = {"ANIMATABLE"},
    override: set = set(),
    poll: Callable[[Self, Context], bool] = None,
    update: Callable[[Self, Context], None] = None,
) -> T:
    # add_file()
    return PointerProperty(
        type=type,
        name=name,
        description=description,
        translation_context=translation_context,
        options=options,
        override=override,
        poll=poll,
        update=update,
    )
