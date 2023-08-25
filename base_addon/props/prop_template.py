from ..helpers.btypes import BPropertyGroup
from bpy.props import BoolProperty
from bpy.types import PropertyGroup, Scene


@BPropertyGroup(Scene, "test_addon")
class TestSettings(PropertyGroup):

    test_prop: BoolProperty("test")


def get_settings(context) -> TestSettings:
    return context.scene.test_addon