from stageflow import Flow
from stageflow import Stage


def test_create_stage():
    Stage()


def test_create_flow_bare():
    flow = Flow()

    assert flow.get_current_stage() is None
    assert set(flow.get_stages()) == set([])


def test_create_flow_and_add_stage():
    flow = Flow()
    flow.add_stage('test', Stage())

    assert flow.get_current_stage() is None
    assert set(flow.get_stages()) == set(['test'])


def test_create_flow_with_stage():
    flow = Flow(stages=dict(test=Stage()))

    assert flow.get_current_stage() is None
    assert set(flow.get_stages()) == set(['test'])


def test_create_flow_with_initial_stage():
    class TestStage():
        def enter(self, data):
            pass
        def exit(self):
            pass

    flow = Flow(
        stages=dict(test=TestStage()),
        initial_stage='test',
    )

    assert flow.get_current_stage() is 'test'
    assert set(flow.get_stages()) == set(['test'])


def test_transition_entry():
    test_data = 'foo'
    global passed_data
    passed_data = None

    class TestStage(Stage):
        def enter(self, data):
            global passed_data
            passed_data = data

    flow = Flow(
        stages=dict(test=TestStage()),
        initial_stage='test',
        initial_stage_data=test_data,
    )

    assert passed_data == test_data
    assert flow.get_current_stage() == 'test'


def test_transition_entry():
    global has_exited
    has_exited = False
    
    exit_data = 'foo_bar_baz'
    global entry_data
    entry_data = None

    class TestStage(Stage):
        def enter(self, data):
            global entry_data
            entry_data = data

        def exit(self, data):
            global has_exited
            has_exited = True
            return exit_data

    flow = Flow(
        stages=dict(
            test_a=TestStage(),
            test_b=TestStage(),
        ),
        initial_stage='test_a',
    )

    assert flow.get_current_stage() == 'test_a'
    assert entry_data is None
    assert not has_exited

    flow.transition('test_b')

    assert flow.get_current_stage() == 'test_b'
    assert entry_data == exit_data
    assert has_exited


def test_pushing_substage():
    global entry_data
    entry_data = None
    global exit_data
    exit_data = None

    class TestStage(Stage):
        def enter(self, data):
            global entry_data
            entry_data = 'stage'
        def exit(self, data):
            global exit_data
            exit_data = 'stage'
        def exit_to_substage(self, substage, data):
            global exit_data
            exit_data = 'stage'
        def reenter_from_substage(self, substage, data):
            global entry_data
            entry_data = 'stage'

    class TestSubstage(Stage):
        def enter(self, data):
            global entry_data
            entry_data = 'substage'
        def exit(self, data):
            global exit_data
            exit_data = 'substage'
        def exit_to_substage(self, data):
            global exit_data
            exit_data = 'substage'
        def reenter_from_substage(self, substage, data):
            global entry_data
            entry_data = 'substage'

    flow = Flow(
        stages=dict(test=TestStage()),
        substages=dict(test_substage=TestSubstage()),
        initial_stage='test',
    )
    assert exit_data is None
    assert entry_data == 'stage'
    assert flow.get_current_substage() is None

    flow.push_substage('test_substage')
    assert exit_data == 'stage'
    assert entry_data == 'substage'
    assert flow.get_current_substage() == 'test_substage'

    flow.pop_substage()
    assert exit_data == 'substage'
    assert entry_data == 'stage'
    assert flow.get_current_substage() is None

# FIXME: Now add the ways that Flow *shouldn't* be usable:
# * transitioning to non-existent stages
# * passing invalid objects to Flow(stages=...)
