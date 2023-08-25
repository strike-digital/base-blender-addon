from bpy.types import AddonPreferences, Context, UILayout


class TESTAddonPreferences(AddonPreferences):
    bl_idname = __package__.split(".")[0]
    layout: UILayout


def get_prefs(context: Context) -> TESTAddonPreferences:
    return context.preferences.addons[__package__.split(".")[0]].preferences
