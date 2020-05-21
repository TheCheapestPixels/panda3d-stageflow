from stageflow import Stage


class Cutscene(Stage):
    """
    The Cutscene stage acts like a movie player, and can be used for
    splash screens and cinematics. It will play a Panda3D `Interval`
    until it has ended, or the player indicates that it should be ended
    by pressing ``escape``. It then transitions to the next stage,
    passing on the data that was passed to :class:`Cutscene.enter`.

    Subclasses of Cutscene need to implement:

    * :class:`Cutscene.setup_credits`
    * :class:`Cutscene.destroy_credits`

    exit_stage
        The stage to exit to; By default ``main menu``. The data passed
        to that stage will be the same that was passed to the cutscene.
    """

    def __init__(self, exit_stage='main menu', splash_args=None):
        self.exit_stage = exit_stage

    def enter(self, data):
        """"""
        self.data = data
        self.player_exit = False
        self.credits = self.setup_credits(data)
        self.credits.start()
        base.accept('escape', self._trigger_exit)
        self.exit_task = base.task_mgr.add(
            self._check_end_of_credits,
            "check end of credits",
            sort=25,
        )

    def exit(self, data):
        """
        """
        return data

    def _trigger_exit(self):
        self.player_exit = True

    def _check_end_of_credits(self, task):
        if self.player_exit or self.credits.isStopped():
            self.credits.finish()
            self.credits = None
            self.destroy_credits()
            base.flow.transition(self.exit_stage, self.data)
            return task.done
        return task.cont

    def setup_credits(self, data):
        """
        Override this to set up the cutscene.

        data
            The data that was passed to :class:`Stage.enter`

        :returns:
            The Panda3D `Interval` that will be played.
        """

        raise NotImplemented

    def destroy_credits(self):
        """
        Tear down the cutscene again. The `Interval` will be dealt with
        automatically.
        """
        raise NotImplemented


class Panda3DSplash(Cutscene):
    """
    A generic splash screen advertising Panda3D.
    """
    def __init__(self, *args, splash_args=None, **kwargs):
        super().__init__(*args, **kwargs)
        if splash_args is None:
            splash_args = {}
        self.splash_args = splash_args

    def setup_credits(self, data):
        """"""
        # Imported here so that you can import other stages from this
        # module without having panda3d-logos installed.
        from panda3d_logos.splashes import RainbowSplash

        self.splash = RainbowSplash(**self.splash_args)
        return self.splash.setup()

    def destroy_credits(self):
        """"""
        self.splash.teardown()
