from wecs.core import System
from wecs.boilerplate import add_systems
from stageflow import Stage


class WECSStage(Stage):
    """
    A stage in a game that uses WECS and its Panda3D boilerplate, so
    your `World` instance will be `base.ecs_world`. It is *not*
    guaranteed to be "clean" (no `Systems` or `Entities` on `enter`),
    nor required to be left so. This allows for having `Systems` that
    run persistently, and the `Entities` on which they run. This way
    you can transition from `WECSStage` to `Cutscene` to `WECSStage`
    without tearing down and rebuilding your scene graph each time; You
    merely exchange the bits that control them.

    To implement this stage, override :class:`WECSStage.setup` and
    `WECSStage.teardown`, and, where applicable,
    `WECSStage.exit_to_substage` and `WECSStage.reenter_from_substage`.

    system_specs
        A specification of systems added to this stage, before `setup`
        is called. Since they are added automatically, they will also
        be removed automatically after `teardown`.
    """
    
    system_specs = []

    def enter(self, data):
        """
        Sets up WECS systems
        """
        for (sort, priority, system) in self.system_specs:
            if issubclass(system, System):
                system = system()
            base.add_system(
                system,
                sort,
                priority=priority,
            )

        self.setup(data)

    def exit(self, data):
        data = self.teardown(data)
        for _, _, system_type in self.system_specs:
            if isinstance(system_type, System):
                system_type = type(system_type)
            base.remove_system(system_type)
        return data

    def exit_to_substage(self, data):
        pass

    def reenter_from_substage(self, data):
        pass

    def setup(self, data):
        """
        Override this to run setup code for your WECS world, in
        particular entities.

        data
            Data passed to :class:`Stage.enter`
        """
        pass

    def teardown(self, data):
        """
        Override this to tear down your WECS world.

        data
            Data passed to :class:`Stage.exit`

        :returns:
            Data that will be passed on to the next stage.
        """
        return data
