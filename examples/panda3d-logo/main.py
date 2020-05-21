from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import LerpFunc
from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DGG

from panda3d_logos.splashes import Colors
from panda3d_logos.splashes import Pattern

from stageflow import Flow
from stageflow import Stage
from stageflow.prefab import Quit
from stageflow.panda3d import Panda3DSplash


class Repeat(Stage):
    def enter(self, data):
        self.btn_repeat = DirectButton(
            text=("Repeat"),
            text_pos=(0, 0.15),
            text_scale=0.2,
            frameSize=(-1, 1, 0.05, 0.35),
            borderWidth=(0.01, 0.01),
            command=self.repeat,
        )
        self.btn_quit = DirectButton(
            text=("Quit"),
            text_pos=(0, -0.25),
            text_scale=0.2,
            frameSize=(-1, 1, -0.35, -0.05),
            borderWidth=(0.01, 0.01),
            command=self.quit,
        )
        self.buttons = [self.btn_repeat, self.btn_quit]

    def exit(self, data):
        for btn in self.buttons:
            btn.destroy()
        return data

    def repeat(self):
        base.flow.transition('splashes')

    def quit(self):
        base.flow.transition('quit')


ShowBase()
base.flow = Flow(
    stages=dict(
        splashes=Panda3DSplash(
            exit_stage='repeat',
            splash_args=dict(
                pattern=Pattern.WHEEL,
                colors=Colors.RAINBOW,
                pattern_freq=1,
                cycle_freq=5,
            ),
        ),
        repeat=Repeat(),
        quit=Quit(),
    ),
    initial_stage='splashes',
)
base.run()
