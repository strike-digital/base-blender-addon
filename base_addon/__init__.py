# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# bl_info = {
#     "name": "BASE_ADDON",
#     "author": "Andrew Stevenson",
#     "description": "TEMP_DESCRIPTION",
#     "blender": (3, 2, 0),
#     "version": (2, 1, 2),
#     "location": "LOCATION",
#     "warning": "",
#     "doc_url": "",
#     "category": "3D View",
# }

# from . import auto_load
from .helpers import btypes

btypes.configure(addon_string="test", auto_register=True)


def register():
    btypes.register()


def unregister():
    btypes.unregister()
