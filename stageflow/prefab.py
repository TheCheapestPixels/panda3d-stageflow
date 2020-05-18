import sys

from stageflow import Stage


class Cutscene(Stage):
    """
    The Cutscene stage acts like a movie player, and can be used for
    splash screens and cinematics. It will play an interval until it
    has ended, or the player indicates that it should be ended. It then
    transitions to the next stage, passing on the data that was passed
    to it.

    Subclasses of Cutscene need to implement:

    * setup_credits(data): Set up the scene. Return an Interval.
    * destroy_credits(): Tear down the scene again. The Interval will be
      dealt with automatically.

    args:
    * exit_stage: The stage to exit to.
    """

    def __init__(self, exit_stage='main menu'):
        self.exit_stage = exit_stage

    def enter(self, data):
        self.data = data
        self.player_exit = False
        self.credits = self.setup_credits(data)
        self.credits.start()
        base.accept('escape', self.trigger_exit)
        self.exit_task = base.task_mgr.add(self.check_end_of_credits, "check end of credits", sort=25)

    def exit(self, data):
        return data

    def trigger_exit(self):
        self.player_exit = True

    def check_end_of_credits(self, task):
        if self.player_exit or self.credits.isStopped():
            self.credits.finish()
            self.credits = None
            self.destroy_credits()
            base.flow.transition(self.exit_stage, self.data)
            return task.done
        return task.cont

    def setup_credits(self, data):
        raise NotImplemented

    def destroy_credits(self):
        raise NotImplemented


class Quit(Stage):
    def enter(self, data):
        sys.exit()
