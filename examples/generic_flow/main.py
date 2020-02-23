from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import LerpFunc

from stageflow import Cutscene
from stageflow import Quit
from stageflow import Flow


ShowBase()
base.disable_mouse()


class StartupSplashes(Cutscene):
    def setup_credits(self, data):
        base.cam.set_pos(0, -10, 0)
        base.cam.look_at(0, 0, 0)
        self.ball = base.loader.load_model("models/smiley")
        self.ball.reparent_to(base.render)
        return LerpFunc(
            self.run_credits,
            fromData=0,
            toData=1,
            duration=5.0,
            blendType='noBlend',
            extraArgs=[],
            name=None,
        )

    def run_credits(self, t):
        self.ball.set_h(t*360*5)

    def destroy_credits(self):
        self.ball.remove_node()


base.flow = Flow(
    stages=dict(
        splashes=StartupSplashes(exit_stage='quit'),
        quit=Quit(),
    ),
    initial_stage='splashes',
)
## Alternative to the above:
#base.flow = Flow()
#base.flow.add_stage('splashes', StartupSplashes(exit_stage='quit'))
#base.flow.add_stage('quit', Quit())
#base.flow.transition('splashes', None)
base.run()
