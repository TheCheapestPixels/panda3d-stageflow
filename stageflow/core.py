class Stage:
    """
    To implement a stage, inherit this class, and override its
    functions. Should any non-overridden function ever be called, that
    will raise an exception, since now the expected behavior is
    undefined.
    """

    def enter(self, data):
        """
        Override this with setup code for entry of this stage.

        data
            Data passed from the exit of the previous :class:`Stage`.

        :returns:
            Returned values will be ignored.
        """
        raise Exception

    def exit(self, data):
        """
        Override this with teardwn code for exit from this stage, and
        pass on data for the next stage.

        data
            Data that was passed to :class:`Flow.transition`.

        :returns:
            Arbitrary data for the next active :class:`Stage`.
        """
        raise Exception

    def exit_to_substage(self, substage, data):
        """
        Override this with code to prepare for this stage's interruption
        by the substage.

        substage
            Name of the interrupting substage.
        data
            Data that was passed to :class:`Flow.push_substage`.

        :returns:
            Returned data will be passed to the substage's 
            :class:`Stage.enter`.
        """
        raise Exception

    def reenter_from_substage(self, substage, data):
        """
        Override this with code that resumes the stage (or whatever
        other action may be required) after the interrupting substage
        has exited.

        substage
            Name of the interrupting substage that has ended.
        data
            Data returned by the the substage's :class:`Stage.exit`.

        :returns:
            Returned values will be ignored.
        """
        raise Exception


class Flow:
    def __init__(self, stages=None, substages=None, initial_stage=None, initial_stage_data=None):
        """
        A container for stages and substages, and managing the flow
        between them.

        stages
            a dictionary `dict(name=StageType())` of your :class:`Stage`
            instances.
        substages
            (optional) another dictionary of stages, to be used as
            substages.
        initial_stage
            (optional) The name of the :class:`Stage` to enter
            immediately. 
        initial_stage_data
            (optional) 
        """
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
        """
        :returns:
            The names of all stages.
        """
        return self.stages.keys()

    def add_stage(self, stage_name, stage):
        self.stages[stage_name] = stage

    def get_current_substage(self):
        if self.active_substages:
            return self.active_substages[-1]
        else:
            return None

    def transition(self, stage_name, data=None):
        """
        Exit the current stage and enter another. This can only be done
        if no substage is active.

        stage_name
            Name of the stage to transition to
        data
            Arbitrary data that will be passed to the current stage's
            :class:`Stage.exit`
        """
        if stage_name not in self.stages:
            raise ValueError("Flow has no stage named '{}'.".format(stage_name))
        if self.active_substages:
            raise Exception("Can not leave a stage with active substages.")
        if self.current_stage is not None:
            final_data = self.stages[self.current_stage].exit(data)
        else:
            final_data = data
        self.current_stage = stage_name
        self.stages[stage_name].enter(final_data)

    def push_substage(self, substage_name, data=None):
        """
        substage_name
            The name of the substage to be entered.
        data
            Arbitrary data that will be passed to the currently active
            (sub-)stage's :class:`Stage.exit_to_substage`.
        """
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
        """
        data
            Arbitrary data that will be passed to the currently active
            (sub-)stage's :class:`Stage.exit`.
        """
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
