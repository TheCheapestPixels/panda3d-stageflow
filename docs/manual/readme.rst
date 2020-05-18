panda3d-stageflow
=================

Just about every game beyond gameplay prototypes goes through distinct
stages: Opening credits, main menu, main game loop, ingame credits, and
so on. These can be arranged as a finite state machine, with data being
passed between stages.

In addition, each stage, especially the main menu and main game loop,
can have certain modes that modify their base functionality, mostly
menus that pause the base game; These are called substages.

``stageflow`` implements this basic framework, letting you… \* focus on
each ``Stage`` and ``Substage`` separately, \* re-use ``Substages`` over
several ``Stages``, \* use premade typical ``Stages`` / ``Substages``.

For example: # FIXME: Abstract Panda3DSplash out of the example…

.. code:: python

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

This example…

-  creates a ``Flow`` with two stages (named ``splashes`` and ``quit``),
-  immediately enters the ``splashes`` stage, which creates a ``Task``,
-  starts Panda3D’s main loop,
-  lets the ``Task`` play the splash until it ends, or ``escape`` is
   pressed,
-  transitions to ``quit``, which in turn ends the program.

Installation, etc.
------------------

Installation: ``pip install panda3d-stageflow``

Documentation: Not yet on readthedocs :( FIXME

Source and issue tracker:
`GitHub <https://github.com/TheCheapestPixels/panda3d-stageflow>`__
