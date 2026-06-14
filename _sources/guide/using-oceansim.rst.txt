Using OceanSim
==============

OceanSim is designed around an external-controller workflow. Godot owns the real-time world state and sensor simulation. Python clients query state, issue controls, visualize plans, and export datasets through the TCP protocol.

Runtime model
-------------

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Layer
     - Responsibilities
   * - Godot runtime
     - Scene update, AUV physics, water/current effects, map generation, sensors, UI, TCP server, and export commands.
   * - TCP protocol
     - Stable command boundary using newline-delimited JSON messages with protocol versioning and request IDs.
   * - Python SDK
     - Connection lifecycle, typed AUV wrapper, sensor validation, coordinate utilities, mapping helpers, and recording/replay tools.

Coordinate frames
-----------------

``AUVState.position`` uses the OceanSim user frame, which is compatible with ROS ENU: ``x=east/right``, ``y=north/forward``, and ``z=up``. Godot uses a Y-up world frame internally.

.. list-table::
   :header-rows: 1
   :widths: 38 62

   * - Conversion
     - Mapping
   * - Godot XYZ to OceanSim / ENU
     - ``[X, -Z, Y]``
   * - OceanSim / ENU to Godot XYZ
     - ``[x, z, -y]``
   * - OceanSim / ENU to ROS NED
     - ``[y, x, -z]``

Use the SDK helpers in :mod:`oceansim_client.coordinates` instead of hand-writing sign flips in controller code.

Workflow patterns
-----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Workflow
     - Recommended API surface
   * - Scripted control
     - ``AUV.set_force()``, ``AUV.set_pose()``, ``AUV.get_state()``, and ``AUV.get_sensors()``.
   * - LLM or MPC navigation
     - ``get_lidar_2d()``, ``get_terrain_grid()``, ``set_nav_path()``, ``set_pred_trajectory()``, and ``set_force()``.
   * - RL online training
     - ``AUV.reset()`` and ``AUV.step(action)``, where each step updates state and sensor observations.
   * - Dataset capture
     - ``OceanSimPklRecorder``, ``AUV.export_dataset()``, ``OceanSimRunReplay``, and robotics export helpers.

Minimal loop
------------

.. code-block:: python

   from oceansim_client import AUV

   with AUV(host="localhost", port=9876) as auv:
       state = auv.get_state()
       print(state.position, state.depth)
       auv.set_force(0.0, 120.0, 0.0)
       sensors = auv.get_sensors()
       print(sensors.keys())
