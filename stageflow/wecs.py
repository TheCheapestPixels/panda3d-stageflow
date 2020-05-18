from wecs.boilerplate import add_systems
from stageflow import Stage


class WECSStage(Stage):
    system_specs = []

    def enter(self, data):
        add_systems(self.system_specs)
        self.create_entities(data)

    def exit(self, data):
        pass
        #self.destroy_entities(data)
        # FIXME: Remove systems

    def exit_to_substage(self, data):
        pass

    def reenter_from_substage(self, data):
        pass
