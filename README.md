panda3d-stageflow
=================

Just about every game beyond gameplay prototypes goes through distinct
stages: Opening credits, main menu, main game loop, ingame credits, and
so on. These can be arranged as a finite state machine, with data being
passed between stages.

In addition, each stage, especially the main menu and main game loop,
can have certain modes that modify their base functionality, mostly
menus that pause the base game; These are called substages.

`stageflow` implements this basic framework, letting you...
* focus on each `Stage` and `Substage` separately,
* re-use `Substages` over several `Stages`,
* use premade typical `Stages` / `Substages`.

For example:
```python
from direct.showbase.ShowBase import ShowBase
from stageflow import Flow
from stageflow.panda3d import Panda3DSplash
from stageflow import Quit


ShowBase()
base.flow = Flow(
    stages=dict(
        splash=Panda3DSplash(exit_stage='quit'),
        quit=Quit(),
    ),
    initial_stage='splash',
)
base.run()
```

This example...
* creates a `Flow` with two stages (named `splashes` and `quit`),
* immediately enters the `splashes` stage, which creates a `Task`,
* starts Panda3D's main loop,
* lets the `Task` play the splash until it ends, or `escape` is pressed,
* transitions to `quit`, which in turn ends the program.


Installation
------------

Not yet: `pip install panda3d-stageflow`
Documentation: None yet.
Source and issue tracker: [GitHub](https://github.com/TheCheapestPixels/panda3d-stageflow)


Tutorial
--------

A `Stage` is a major segment of a game. `Stages`...
* are mutually non-overlapping; There is exactly one active `Stage` at
  any time while the game is running,
* have an `Stage.enter(data)` method that sets up, and an
  `Stage.exit(data)` method that tears down the `Stage`.

A `Flow`...
* is the container for a game's `States`, each stored under a name,
* has a `Flow.transition(stage, data)` method that exits the current
  `Stage` and enters the target stage,
* is fully and reflexively conected; It may transition from any `Stage`
  to any other, including the current one (basically restarting it),
* manages how data is passed on, to allow for limited communication
  between `Stages`; `Flow.transition(stage, data)` passes the `data` on
  to `current_stage.exit(data)`, and the data returned by that method is
  passed to `target_stage.enter(data)`.

Let's see that in action:

```python
from stageflow import Flow
from stageflow import Stage


class MyStage(Stage):
    def enter(self, data):
        # Set uo the Stage here
        print("MyStage.enter({})".format(data))

    def exit(self, data):
        # Tear down stage, and return data to be passed on
        print("MyStage.exit({})".format(data))
        return "Data returned by MyStage.exit()"


flow = Flow(
    stages=dict(
        mystage=MyStage(),
    ),
)


flow.transition('mystage', "Argument to flow.transition")
# Output:
#     MyStage.enter(Argument to flow.transition)


flow.transition('mystage', "Argument to flow.transition")
# Output:
#     MyStage.exit(Argument to flow.transition)
#     MyStage.enter(Data returned by MyStage.exit())
```

We can also enter a `Stage` automatically when creating the `Flow`:
```python
flow = Flow(
    stages=dict(
        mystage=MyStage(),
    ),
    initial_stage='stages',
    initial_stage_data='Initial data from Flow creation',
)
# Output:
#     MyStage.enter(Initial data from Flow creation)
```

`Substages` are temporary interruptions to the underlying stage. They
stack one on top of another, and also need to be unstacked in reverse
order. While `Substages` are present, the current `Stage` can not be
transitioned out of.

`Flow` provides the methods `Flow.push_substage(stage, data)` and
`Flow.pop_substage(data)` to add and remove substages. `Stages` and
`Substages` (which are, under the hood, the same) provide
`exit_to_substage(data)` and `reenter_from_substage(data)` methods to do
appropriate actions to pause and unpause the `Stage` or `Substage`.

The `Substage` pushed "on top", however, will still be entered / exited
using its `enter` / `exit` methods when moving from / to the stage
"below".

```python
from stageflow import Flow
from stageflow import Stage


class MyStage(Stage):
    def __init__(self, stage_name):
        self.stage_name = stage_name

    def enter(self, data):
        print("{}.enter({})".format(self.stage_name, data))

    def exit(self, data):
        print("{}.exit({})".format(self.stage_name, data))
        return "Data returned by {}.exit()".format(self.stage_name)

    def exit_to_substage(self, substage, data):
        print("{}.exit_to_substage({}, {})".format(
            self.stage_name,
            substage,
            data,
        ))
        return "Data returned by {}.exit_to_substage()".format(
            self.stage_name,
        )

    def reenter_from_substage(self, substage, data):
        print("{}.reenter_from_substage({}, {})".format(
            self.stage_name,
            substage,
            data,
        ))


flow = Flow(
    stages=dict(
        mystage=MyStage("BaseStage"),
    ),
    substages=dict(
        substage_a=MyStage("SubstageA"),
        substage_b=MyStage("SubstageB"),
    ),
    initial_stage='mystage',
)
# Output:
#     BaseStage.enter(None)

flow.push_substage('substage_a', "Argument to flow.push_substage")
# Output:
#     BaseStage.exit_to_substage(substage_a, Argument to flow.push_substage)
#     SubstageA.enter(Data returned by BaseStage.exit_to_substage())

flow.push_substage('substage_b', "Argument to flow.push_substage")
# Output:
#     SubstageA.exit_to_substage(substage_b, Argument to flow.push_substage)
#     SubstageB.enter(Data returned by SubstageA.exit_to_substage())

flow.pop_substage("Argument to flow.pop_substage")
# Output:
#     SubstageB.exit(Argument to flow.pop_substage)
#     SubstageA.reenter_from_substage(substage_b, Data returned by SubstageB.exit())

flow.pop_substage("Argument to flow.pop_substage") 
# Output:
#     SubstageA.exit(Argument to flow.pop_substage)
#     BaseStage.reenter_from_substage(substage_a, Data returned by SubstageA.exit())
```


Out-of-the-box stages
---------------------

* `prefab`
  * `Cutscene`: Plays a Panda3D `Interval`
  * `Quit`: `Quit.enter` calls `sys.exit()`
* `panda3d`
  * `Panda3DSplash`: A `Cutscene` advertising Panda3D
* `wecs`
  *`WECSStage`: (FIXME: not ready) Set up / tear down a WECS world


TODO
====

* API docs
* Tests for misusing the API
* Re-type Exceptions
* CLI args for initial stage and data, overriding setup in code
* Stages
  * WECSStage
  * Abstract more Stages out of examples
* Package
