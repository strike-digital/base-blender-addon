import importlib
import inspect
from pathlib import Path
from typing import Callable, Concatenate, ParamSpec, Self, TypeVar

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
from bpy.types import AddonPreferences, Context, Operator, PropertyGroup

"""
This is my attempt at a method of defining Blender properties while maintaining useful type hinting.
I have no idea if it's worth it, or if it's massive overkill, but it does make me feel better.

Some notes:
    - properties need to be defined using the "=" sign rather than the ":" sign
      (this is because type hints aren't propagated through function calls)
"""


files = set()


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
            add_file()
            return fun(*args, **kwargs)

        return decorated

    return decorator


def add_file():
    """Add a file to the list for having BProperties converted into regular properties"""
    files.add(inspect.stack()[2].filename)


@override_prop_return(StringProperty)
def BStringProperty(*args, **kwargs) -> str: ...


@override_prop_return(EnumProperty)
def BEnumProperty(*args, **kwargs) -> str: ...


@override_prop_return(IntProperty)
def BIntProperty(*args, **kwargs) -> int: ...


@override_prop_return(IntVectorProperty)
def BIntVectorProperty(*args, **kwargs) -> list[int]: ...


@override_prop_return(BoolProperty)
def BBoolProperty(*args, **kwargs) -> bool: ...


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
    add_file()
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


def register():
    """Import the files that the BProperties are defined in, and convert them from values into annotations"""
    deferred_prop = type(IntProperty())

    package_name = __package__.split(".")[0]
    package_module = importlib.import_module(package_name)
    for file in files:
        if file.startswith("<frozen"):  # Ignore this file for testing
            continue
        package_module.__file__
        relative_path = Path(file).relative_to(Path(package_module.__file__).parent)
        relative_path = relative_path.parent / relative_path.stem
        module_path = package_name + "." + ".".join(relative_path.parts)
        module = importlib.import_module(module_path)

        classes = []
        inheritors = {PropertyGroup, Operator, AddonPreferences}
        for value in module.__dict__.values():
            if not inspect.isclass(value):
                continue

            for inheritor in inheritors:
                if issubclass(value, inheritor):
                    break
            else:
                continue
            classes.append(value)

        # classes = [v for v in module.__dict__.values() if inspect.isclass(v) and issubclass(v, PropertyGroup)]
        for cls in classes:
            if cls.__module__ != module_path:
                continue

            # for key, value in list(cls.__dict__.items()):
            for key in dir(cls):
                if key.startswith("__"):
                    continue
                value = getattr(cls, key)
                if issubclass(type(value), deferred_prop):
                    cls.__annotations__[key] = value
