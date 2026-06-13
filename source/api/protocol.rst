TCP Protocol
============

The simulator exposes a newline-delimited JSON TCP protocol. Each request is one JSON object followed by ``\n``. Protocol version ``2`` adds request IDs, typed response envelopes, status fields, and batch support.

Wire format
-----------

.. code-block:: json

   {
     "type": "command",
     "protocol_version": 2,
     "request_id": "run-001",
     "action": "get_state"
   }

Envelopes
---------

.. list-table::
   :header-rows: 1
   :widths: 28 24 48

   * - Field
     - Applies to
     - Description
   * - ``type``
     - request/response
     - ``command``, ``sim_control``, ``batch``, ``state``, ``response``, or ``error``.
   * - ``protocol_version``
     - request/response
     - Current value is ``2``.
   * - ``request_id``
     - request/response
     - Optional client-provided correlation ID. Responses preserve it when present.
   * - ``action``
     - request/response
     - Command name such as ``get_state``, ``set_force``, or ``export_dataset``.
   * - ``data``
     - request/response
     - Action payload or action result.
   * - ``status`` / ``success``
     - response
     - ``ok`` / ``true`` or ``error`` / ``false``.
   * - ``sim_time``
     - response
     - Simulation time included in state and protocol context responses.

Action summary
--------------

.. list-table::
   :header-rows: 1
   :widths: 34 20 46

   * - Action
     - Type
     - Purpose
   * - ``get_state``
     - command
     - Return AUV state and embedded sensor data.
   * - ``get_sensors``
     - command
     - Return active sensor payloads.
   * - ``step``
     - command
     - Apply a force or thruster command and return updated state.
   * - ``set_force``
     - command
     - Compatibility alias for world-frame force control.
   * - ``set_force_world``, ``set_force_body``
     - command
     - Apply a three-axis force in world frame or AUV body frame.
   * - ``set_body_wrench``, ``set_body_velocity``
     - command
     - Apply six-degree body-frame control inputs.
   * - ``set_thrust``, ``set_thrusters``
     - command
     - Set named thruster values from a profile-level control dictionary.
   * - ``reset``, ``pause``, ``resume``, ``set_time_scale``
     - sim_control
     - Control global simulation state.
   * - ``set_scenario``, ``generate_map``, ``get_map_info``, ``get_terrain_grid``
     - command
     - Load scenarios and query map data.
   * - ``spawn_obstacle``, ``remove_obstacle``
     - command
     - Manage static obstacles.
   * - ``spawn_agent``, ``move_agent``, ``remove_agent``, ``clear_agents``, ``get_agents``
     - command
     - Manage dynamic AUV-like agents.
   * - ``set_nav_path``, ``set_waypoint``, ``set_pred_trajectory``, ``set_waypoints``, ``clear_nav``
     - command
     - Drive simulator-side navigation overlays.
   * - ``export_dataset``, ``save_snapshot_json``
     - command
     - Export run artifacts or a snapshot JSON.

Command details
---------------

.. py:function:: get_state()

   Return the current AUV state. The response type is ``state``, not a generic response, and the payload includes ``position``, ``velocity``, ``depth``, ``speed``, ``heading_deg``, ``sim_time``, and ``sensors``.

   :returns: ``{type: "state", status: "ok", data: State}``

.. py:function:: get_sensors()

   Return the active sensor dictionary. This is useful when the controller needs fresh sensor payloads without manually unpacking the full state object.

   :returns: state response whose data contains ``sensors``.

.. py:function:: step(data)

   Apply ``data.force`` or ``data.thrusters``, advance the control loop, and return state. This is the preferred online-training request because one round trip provides action execution and observation.

   :param data: ``{"force": [fx, fy, fz]}`` or ``{"thrusters": {...}}``.
   :returns: updated state response with sensor payloads.

.. py:function:: set_force(data)

   Compatibility alias for world-frame force control, where ``x`` is
   lateral/right, ``y`` is forward, and ``z`` is up.

   :param data: ``{"force": [fx, fy, fz]}``
   :returns: generic ``response`` envelope.

.. py:function:: set_force_world(data)

   Apply ``{"force": [fx, fy, fz]}`` in OceanSim world/user coordinates.

.. py:function:: set_force_body(data)

   Apply ``{"force": [fx, fy, fz]}`` in the AUV body frame.

.. py:function:: set_body_wrench(data)

   Apply ``{"wrench": [fx, fy, fz, tx, ty, tz]}`` in the AUV body frame.

.. py:function:: set_body_velocity(data)

   Apply ``{"velocity": [u, v, w, p, q, r]}`` as body-frame linear and angular
   velocity components.

.. py:function:: set_scenario(data)

   Load a named scenario and regenerate the map.

   :param data: ``{"scenario": "NarrowMap", "seed": 0}``
   :returns: map metadata returned by the map manager.

.. py:function:: get_terrain_grid(data)

   Return a 2D occupancy grid for classical planners. The grid uses ``1=blocked`` and ``0=free``; ``class_grid`` may distinguish terrain, static obstacles, and dynamic agents.

   :param data: ``cell_size``, ``auv_y``, ``include_static_obstacles``, ``include_dynamic_agents``, and ``inflation_radius``.

.. py:function:: export_dataset(data)

   Export point-cloud run artifacts through the simulator. The Python wrapper waits up to 60 seconds because export can be slower than ordinary control commands.

   :param data: ``{"export_dir": optional, "render_image": bool, "pack_dataset": bool}``
   :returns: paths and export status.

Batch requests
--------------

Batch requests wrap multiple command or sim-control objects into one TCP request. The simulator returns a response containing ``count`` and a ``responses`` array. The current batch limit is ``64`` requests.

.. code-block:: json

   {
     "type": "batch",
     "protocol_version": 2,
     "request_id": "batch-001",
     "requests": [
       {"type": "command", "action": "get_state"},
       {"type": "command", "action": "set_force", "data": {"force": [0, 100, 0]}}
     ]
   }

Errors
------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Error code
     - Meaning
   * - ``unknown_type``
     - The request ``type`` is not supported.
   * - ``unknown_action``
     - The request action is not recognized for its type.
   * - ``invalid_message``
     - The request is malformed or the action payload failed validation.
   * - ``invalid_action_shape``
     - A vector action has the wrong length or contains non-numeric values.
   * - ``unknown_agent``
     - The requested runtime agent ID is not registered.
   * - ``unsupported_control_scheme``
     - The agent exists but does not support the requested control path.
   * - ``spawn_failed`` / ``blocked_pose``
     - Runtime placement failed or the target pose is blocked.
   * - ``batch_limit``
     - The batch request contains too many child requests.
