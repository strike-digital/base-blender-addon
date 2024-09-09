from bpy.props import BoolProperty
from bpy.types import PropertyGroup, Scene

from ..helpers.bprops import BBoolProperty, BStringProperty
from ..helpers.btypes import BPropertyGroup


@BPropertyGroup(Scene, "test_addon")
class TestSettings(PropertyGroup):

    test_prop: BoolProperty("test")

    hoho = BBoolProperty("haha")

    haha = BStringProperty()


# print(TestSettings.haha)
TestSettings.haha.draw("haha", "hoho")


def get_settings(context) -> TestSettings:
    return context.scene.test_addon
