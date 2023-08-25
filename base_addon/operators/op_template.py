from bpy.types import Context
from ..helpers.btypes import BOperator


@BOperator("test")
class TEST_OT_test_op(BOperator.type):
    """Testing!"""

    def execute(self, context: Context):
        print("testing")