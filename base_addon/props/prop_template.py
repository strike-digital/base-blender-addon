from bpy.types import PropertyGroup, Scene

from ..helpers.btypes import BBoolProperty, BPropertyGroup


@BPropertyGroup(Scene, "test_addon")
class TestSettings(PropertyGroup):

    test_prop = BBoolProperty("test")


def get_settings(context) -> TestSettings:
    return context.scene.test_addon
