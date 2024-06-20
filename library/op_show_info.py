from dataclasses import dataclass

import blf

from bpy.props import IntProperty, BoolProperty, StringProperty
from bpy.types import Context, UILayout

from ..helpers.btypes import BOperator


def wrap_text(
    context: Context,
    text: str,
    layout: UILayout,
    centered: bool = False,
    width=0,
    splitter=None,
) -> list[str]:
    """Take a string and return a list of lines so that it fits within the given width (defaults to region width)"""
    return_text = []
    row_text = ""

    width = width or context.region.width
    system = context.preferences.system
    ui_scale = system.ui_scale
    width = (4 / (5 * ui_scale)) * width

    blf.size(0, 11)

    for word in text.split(splitter):
        if word == "":
            return_text.append(row_text)
            row_text = ""
            continue
        word = f" {word}"
        line_len, _ = blf.dimensions(0, row_text + word)

        if line_len <= (width - 16):
            row_text += word
        else:
            return_text.append(row_text)
            row_text = word

    if row_text:
        return_text.append(row_text)

    for text in return_text:
        row = layout.row()
        if centered:
            row.alignment = "CENTER"
        row.label(text=text)

    return return_text


@BOperator()
class AT_OT_show_info(BOperator.type):
    title: StringProperty()

    message: StringProperty()

    icon: StringProperty()

    show_content: BoolProperty()

    width: IntProperty(default=300)

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=self.width)

    def draw(self, context):
        layout = self.layout
        column = layout.column(align=True)
        box = column.box().row(align=True)
        box.alignment = "CENTER"
        offset = "" if self.icon else "    "
        box.label(text=self.title + offset, icon=self.icon)

        box = column.box().column(align=True)
        message = self.message.replace("  ", "").replace("\n", " ")
        wrap_text(context, message, box, width=self.width * 1.25, splitter=" ")


@dataclass
class InfoSnippet:
    title: str
    message: str
    icon: str = "NONE"

    def draw(self, layout: UILayout, icon_override=""):
        op = AT_OT_show_info.draw_button(layout, text="", icon=icon_override or "INFO")
        op.title = self.title
        op.message = self.message
        op.icon = self.icon


class InfoSnippets:
    my_snippet = InfoSnippet(
        "My Snippet",
        """\
        My text.\n
        More text \
        Continued text.
        """,
        icon="FILE_FOLDER",
    )
