from typing import TYPE_CHECKING, Any

from bpy.types import NodeTree


class BDict(dict):
    """Used to mimic the behavior of the built in Collection Properties in Blender, which act as a
    mix of dictionaries and lists."""

    def __iter__(self):
        return iter(self.values())

    def __getitem__(self, __key: Any) -> Any:
        if isinstance(__key, int):
            return list(self.values())[__key]
        return super().__getitem__(__key)


class BNodeTree(NodeTree if TYPE_CHECKING else object):
    """A wrapper for the new 4.0 node tree api, allowing easier access to attributes such as inputs and outputs"""

    # Boilerplate
    def __init__(self, node_tree: NodeTree):
        self.tree = node_tree

    def __str__(self) -> str:
        return f"BNodeTree({self.tree.__str__()})"

    def __repr__(self) -> str:
        return self.__str__()

    def __getattribute__(self, __name: str) -> Any:
        """check if attribute is on either the wrapper or the node tree, otherwise error."""
        try:
            return super().__getattribute__(__name)
        except AttributeError as e:
            try:
                return getattr(self.tree, __name)
            except AttributeError:
                raise e

    @property
    def panels(self):
        return BDict({s.identifier: s for s in self.tree.interface.items_tree if s.item_type == "PANEL"})

    @property
    def sockets(self):
        return BDict({s.identifier: s for s in self.tree.interface.items_tree if s.item_type == "SOCKET"})

    @property
    def inputs(self):
        return BDict({s.identifier: s for s in self.sockets if s.in_out == "INPUT"})

    @property
    def outputs(self):
        return BDict({s.identifier: s for s in self.sockets if s.in_out == "OUTPUT"})
