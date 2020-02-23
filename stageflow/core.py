class Stage:
    def enter(self, data):
        raise Exception

    def exit(self, data):
        raise Exception

    def exit_to_substage(self, data):
        raise Exception

    def reenter_from_substage(self, data):
        raise Exception


class Substage(Stage):
    pass


class Flow:
    def __init__(self, stages=None, initial_stage=None, initial_stage_data=None, substages=None):
        self.current_stage = None
        if stages is None:
            self.stages = {}
        else:
            self.stages = stages

        self.active_substages = []
        if substages is None:
            self.substages = {}
        else:
            self.substages = substages

        if initial_stage is not None:
            self.transition(initial_stage, initial_stage_data)

    def get_current_stage(self):
        return self.current_stage

    def get_stages(self):
        return self.stages.keys()

    def add_stage(self, stage_name, stage):
        self.stages[stage_name] = stage

    def get_current_substage(self):
        if self.active_substages:
            return self.active_substages[-1]
        else:
            return None

    def transition(self, stage_name, data=None):
        if stage_name not in self.stages:
            raise ValueError("Flow has no stage named '{}'.".format(stage_name))
        if self.active_substages:
            raise Exception("Can not leave a stage with active substages.")
        if self.current_stage is not None:
            final_data = self.stages[self.current_stage].exit(data)
        else:
            final_data = None
        self.current_stage = stage_name
        self.stages[stage_name].enter(final_data)

    def push_substage(self, substage_name, data=None):
        if substage_name not in self.substages:
            raise ValueError(
                "Flow has no substage named '{}'.".format(substage_name),
            )

        # Exit current stage
        if self.get_current_substage() is None:
            stage = self.stages[self.get_current_stage()]
        else:
            stage = self.substages[self.get_current_substage()]
        data = stage.exit_to_substage(substage_name, data)

        # Enter new substage
        self.active_substages.append(substage_name)
        self.substages[substage_name].enter(data)

    def pop_substage(self, data=None):
        if not self.active_substages:
            raise Exception("No active substage.")

        # Exit current substage
        leaving_substage = self.get_current_substage()
        stage = self.substages[leaving_substage]
        data = stage.exit(data)
        self.active_substages = self.active_substages[:-1]

        # Enter underlying stage
        if not self.active_substages:
            stage = self.stages[self.get_current_stage()]
        else:
            stage = self.substages[self.get_current_substage()]
        stage.reenter_from_substage(leaving_substage, data)
