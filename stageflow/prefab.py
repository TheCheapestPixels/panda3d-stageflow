import sys

from stageflow import Stage


class Quit(Stage):
    """
    Upon :class:`Quit.enter`, `sys.exit()` will be called.
    """

    def enter(self, data):
        """"""
        sys.exit()
