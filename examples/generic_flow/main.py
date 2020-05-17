from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import LerpFunc
from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DGG

from stageflow import Flow
from stageflow import Stage
from stageflow import Cutscene
from stageflow import Quit


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


class MainMenu(Stage):
    def enter(self, data):
        self.btn_quit = DirectButton(
            text=(
                "Quit",
                "Quit!",
                "Quit?",
                "(Quit)",
            ),
            text_pos=(0, -0.7),
            text_scale=0.2,
            frameSize=(-1, 1, -0.8, -0.5),
            borderWidth=(0.01, 0.01),
            command=self.quit,
        )
        self.btn_credits = DirectButton(
            text=(
                "Credits",
                "Credits!",
                "Credits?",
                "(Credits)",
            ),
            text_pos=(0, -0.3),
            text_scale=0.2,
            frameSize=(-1, 1, -0.4, -0.1),
            borderWidth=(0.01, 0.01),
            command=self.credits,
        )
        self.btn_main_game = DirectButton(
            text=(
                "Main Game Loop",
                "Main Game Loop!",
                "Main Game Loop?",
                "(Main Game Loop)",
            ),
            text_pos=(0, 0.6),
            text_scale=0.2,
            frameSize=(-1, 1, 0.5, 0.8),
            borderWidth=(0.01, 0.01),
            command=self.main_game_loop,
        )
        self.buttons = [self.btn_quit, self.btn_credits, self.btn_main_game]

    def exit(self, data):
        for btn in self.buttons:
            btn.destroy()
        return data

    def exit_to_substage(self, substage, data):
        for btn in self.buttons:
            btn["state"] = DGG.DISABLED
        return data

    def reenter_from_substage(self, substage, data):
        for btn in self.buttons:
            btn["state"] = DGG.NORMAL
        if substage == 'are_you_sure':
            question, i_am_sure = data
            if question == 'quit' and i_am_sure:
                base.flow.transition('quit')

    def main_game_loop(self):
        base.flow.transition('main_game_loop')

    def credits(self):
        base.flow.transition('main_credits')

    def quit(self):
        base.flow.push_substage('are_you_sure', 'quit')


class MainGameLoop(Stage):
    def enter(self, data):
        self.btn_menu = DirectButton(
            text=(
                "Ingame Menu",
                "Ingame Menu",
                "Ingame Menu",
                "(Ingame Menu)",
            ),
            text_pos=(0, -0.05),
            text_scale=0.2,
            frameSize=(-1, 1, -0.15, 0.15),
            borderWidth=(0.01, 0.01),
            command=self.ingame_menu,
        )

    def exit(self, data):
        self.btn_menu.destroy()
        return data

    def exit_to_substage(self, substage, data):
        for btn in [self.btn_menu]:
            btn["state"] = DGG.DISABLED
        return data

    def reenter_from_substage(self, substage, data):
        for btn in [self.btn_menu]:
            btn["state"] = DGG.NORMAL
        if data == 'main_menu':
            base.flow.transition('main_menu')
        if data == 'quit':
            base.flow.transition('quit')

    def ingame_menu(self):
        base.flow.push_substage('ingame_menu')


class AreYouSure(Stage):
    def enter(self, data):
        self.btn_yes = DirectButton(
            text=("Yes", "Yes", "Yes", "Yes"),
            text_pos=(-0.6, -0.05),
            text_scale=0.2,
            frameSize=(-1, -0.2, -0.2, 0.2),
            borderWidth=(0.01, 0.01),
            command=self.yes,
        )
        self.btn_no = DirectButton(
            text=("No", "No", "No", "No"),
            text_pos=(0.6, -0.05),
            text_scale=0.2,
            frameSize=(0.2, 1, -0.2, 0.2),
            borderWidth=(0.01, 0.01),
            command=self.no,
        )
        self.data = data

    def exit(self, data):
        self.btn_yes.destroy()
        self.btn_no.destroy()
        return (self.data, data)

    def yes(self):
        base.flow.pop_substage(True)

    def no(self):
        base.flow.pop_substage(False)


class IngameMenu(Stage):
    def enter(self, data):
        self.btn_quit = DirectButton(
            text=(
                "Quit",
                "Quit!",
                "Quit?",
                "(Quit)",
            ),
            text_pos=(0, -0.3),
            text_scale=0.2,
            frameSize=(-1, 1, -0.4, -0.1),
            borderWidth=(0.01, 0.01),
            command=self.quit,
        )
        self.btn_main = DirectButton(
            text=(
                "Main Menu",
                "Main Menu!",
                "Main Menu?",
               "(Main Menu)",
            ),
            text_pos=(0, 0.1),
            text_scale=0.2,
            frameSize=(-1, 1, 0.0, 0.3),
            borderWidth=(0.01, 0.01),
            command=self.main,
        )
        self.btn_back = DirectButton(
            text=(
                "Back",
                "Back!",
                "Back?",
                "(Back)",
            ),
            text_pos=(0, -0.7),
            text_scale=0.2,
            frameSize=(-1, 1, -0.8, -0.5),
            borderWidth=(0.01, 0.01),
            command=self.back,
        )
        self.buttons = [self.btn_main, self.btn_quit, self.btn_back]

    def exit(self, data):
        for btn in self.buttons:
            btn.destroy()
        return data

    def exit_to_substage(self, substage, data):
        for btn in self.buttons:
            btn["state"] = DGG.DISABLED
        return data

    def reenter_from_substage(self, substage, data):
        for btn in self.buttons:
            btn["state"] = DGG.NORMAL
        if substage == 'are_you_sure':
            question, i_am_sure = data
            if question == 'quit' and i_am_sure:
                base.flow.pop_substage('quit')
            if question == 'main' and i_am_sure:
                base.flow.pop_substage('main_menu')

    def main(self):
        base.flow.push_substage('are_you_sure', 'main')

    def quit(self):
        base.flow.push_substage('are_you_sure', 'quit')

    def back(self):
        base.flow.pop_substage()


base.flow = Flow(
    stages=dict(
        splashes=StartupSplashes(exit_stage='main_menu'),
        main_menu=MainMenu(),
        main_game_loop=MainGameLoop(),
        main_credits=StartupSplashes(exit_stage='main_menu'),
        quit=Quit(),
    ),
    substages=dict(
        are_you_sure=AreYouSure(),
        ingame_menu=IngameMenu(),
    ),
    initial_stage='splashes',
)
## Alternative to the above:
#base.flow = Flow()
#base.flow.add_stage('splashes', StartupSplashes(exit_stage='quit'))
#base.flow.add_stage('quit', Quit())
#base.flow.transition('splashes', None)
base.run()
