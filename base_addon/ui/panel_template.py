from bpy.types import Panel

from ..helpers.btypes import BPanel
from ..props.prop_template import TestSettings, get_settings


@BPanel("VIEW_3D", "UI", category="Testing")
class TEST_PT_panel(Panel):

    def draw(self, context):
        layout = self.layout
        layout.label(text="Test Panel!")

        TestSettings.dog.draw(layout, get_settings(context))
