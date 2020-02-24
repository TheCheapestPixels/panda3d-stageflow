panda3d-stageflow
=================

Just about every game beyond gameplay prototypes goes through distinct
stages: Opening credits, main menu, main game loop, ingame credits, and
so on. These can be arranged as a finite state machine, with data being
passed between stages.

In addition, each stage, especially the main menu and main game loop,
can have certain modes that modify their base functionality, mostly
menus that pause the base game.

`stageflow` implements this basic framework.

    from stageflow import Flow, Stage

    # FIXME: Example goes here


Installation
------------

Not yet: `pip install panda3d-stageflow`


TODO
====

* Document basic API use
* Tests for misusing the API
* Re-type Exceptions
* WECSStage
* Docstrings
* CLI args for initial stage and data
* Package
* abstract Stages out of examples
