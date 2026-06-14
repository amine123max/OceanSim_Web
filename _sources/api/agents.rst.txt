Agent API
=========

The ``oceansim_client.agents`` module provides a typed layer over the existing
TCP protocol. It does not replace the ``AUV`` wrapper; it gives experiments a
stable vocabulary for agent definitions, action spaces, and runtime control.

Classes
-------

.. py:class:: AgentDefinition

   Serializable description of a runtime agent.

   .. list-table::
      :header-rows: 1
      :widths: 32 68

      * - Field
        - Meaning
      * - ``agent_name``
        - Stable runtime identifier, for example ``auv/main`` or ``target_01``.
      * - ``agent_type``
        - Logical type such as ``auv`` or ``proxy_auv``.
      * - ``is_main_agent``
        - Whether the definition binds to the scene-owned AUV or spawns a proxy agent.
      * - ``profile``
        - Optional vehicle or runtime profile name.
      * - ``location`` / ``rotation``
        - Initial pose fields.
      * - ``control_scheme``
        - One of the documented ``ControlScheme`` values.
      * - ``sensors``
        - Optional sensor declarations. Entries may be sensor names or
          dictionaries with ``name`` and ``sensor_type``.
      * - ``metadata``
        - Role, semantic label, tags, and experiment-specific annotations.

   .. py:method:: from_dict(data)

      Build an ``AgentDefinition`` from a dictionary. The parser accepts common
      aliases such as ``id``/``name`` and ``position``/``location``.

   .. py:method:: to_dict()

      Return a versioned dictionary suitable for scenario files or protocol
      payloads.

.. py:class:: ActionSpace

   Machine-readable action vector contract. It records ``shape``, ``fields``,
   ``units``, ``frame``, optional bounds, and a short description.

   .. py:method:: validate(action)

      Validate action length and optional bounds, then return a list of floats.

.. py:class:: OceanSimAgent

   Runtime facade bound to an ``OceanSimClient`` and an ``AgentDefinition``.

   .. list-table::
      :header-rows: 1
      :widths: 36 64

      * - Method or property
        - Role
      * - ``name``
        - Runtime identifier.
      * - ``control_scheme``
        - Active control contract.
      * - ``action_space``
        - ``ActionSpace`` for the current control scheme.
      * - ``act(action)``
        - Validate and dispatch an action through TCP.
      * - ``clear_action()``
        - Send a zero action for the current control scheme.
      * - ``teleport(location, rotation=None)``
        - Reposition the main AUV or dynamic proxy agent.
      * - ``agent_state_dict()``
        - Return a dictionary with definition metadata and the latest state.

.. py:class:: AgentFactory

   Factory for binding definitions to live simulator objects.

   .. py:method:: build_agent(client_or_auv, definition, spawn=True)

      Accepts either an ``OceanSimClient`` or ``AUV`` instance. Main agents are
      bound to the existing vehicle; non-main agents can be spawned through the
      current ``spawn_agent`` protocol action.

Control schemes
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 32 38

   * - Name
     - Fields
     - Protocol mapping
   * - ``force_3d``
     - ``fx, fy, fz``
     - ``set_force_world``
   * - ``body_force_3d``
     - ``fx, fy, fz``
     - ``set_force_body``
   * - ``thrusters``
     - ``thruster_0 ...`` from the active vehicle profile
     - ``set_thrusters``
   * - ``external_velocity``
     - ``vx, vy, vz``
     - ``set_agent_velocity``
   * - ``waypoint_pid``
     - ``world_x, world_z, depth``
     - ``set_waypoint`` with controller metadata
   * - ``body_wrench_6dof``
     - ``fx, fy, fz, tx, ty, tz``
     - Six-degree body wrench contract
   * - ``body_velocity_6dof``
     - ``u, v, w, p, q, r``
     - Six-degree body velocity contract
   * - ``custom_dynamics_6dof``
     - ``lin_ax, lin_ay, lin_az, ang_ax, ang_ay, ang_az``
     - Reserved protocol extension

``list_control_schemes()`` returns a machine-readable version of the same
contracts:

.. code-block:: python

   from oceansim_client import list_control_schemes

   for item in list_control_schemes():
       print(item["name"], item["action_space"]["fields"])

Example output:

.. code-block:: text

   force_3d ['fx', 'fy', 'fz']
   body_force_3d ['fx', 'fy', 'fz']
   thrusters ['thruster_0', 'thruster_1', 'thruster_2', 'thruster_3', 'thruster_4', 'thruster_5']
   external_velocity ['vx', 'vy', 'vz']
   waypoint_pid ['world_x', 'world_z', 'depth']
   body_wrench_6dof ['fx', 'fy', 'fz', 'tx', 'ty', 'tz']
   body_velocity_6dof ['u', 'v', 'w', 'p', 'q', 'r']
   custom_dynamics_6dof ['lin_ax', 'lin_ay', 'lin_az', 'ang_ax', 'ang_ay', 'ang_az']

Bounds and vehicle profiles
---------------------------

``ActionSpace`` supports optional ``low`` and ``high`` bounds. The default
contracts define shape, fields, units, frame, and description. Bounds are kept
optional because some values depend on the active vehicle profile, actuator
configuration, controller gains, and scenario-specific safety limits.

The recommended rule is:

* fixed vector shape, field names, units, and frame live in
  ``oceansim_client.agents.ACTION_SPACES``;
* actuator-specific bounds, rate limits, deadbands, and failure modes should be
  derived from ``vehicle_profiles/*.json`` fields such as
  ``command_bounds``, ``rate_limit_per_s``, ``deadband``,
  ``failure_mode``, and ``failure_scale``;
* experiment-specific safety bounds should be written into scenario metadata or
  controller configuration.

Vehicle profiles can expose Fossen-style six-degree dynamics metadata for
controller design and export auditing: rigid-body mass matrix, added-mass
matrix, total mass matrix, damping vectors, restoring force/torque
coefficients, Coriolis matrix/state terms, and the thruster allocation matrix.
The runtime/profile field names are documented as ``rigid_body_mass_matrix``,
``added_mass_matrix``, ``total_mass_matrix``, ``coriolis_matrix``,
``coriolis_force_torque_body``, ``restoring_force_torque_body``,
``restoring_torque_body``, and ``thruster_allocation_matrix``.

.. list-table::
   :header-rows: 1
   :widths: 32 68

   * - Field
     - Meaning
   * - ``command_bounds``
     - Per-actuator minimum and maximum normalized command.
   * - ``rate_limit_per_s``
     - Maximum actuator command change per second.
   * - ``deadband``
     - Small command region treated as zero input.
   * - ``failure_mode``
     - Actuator health model, such as healthy, disabled, stuck, or scaled.
   * - ``failure_scale``
     - Multiplicative actuator scale used by scaled failure cases.
   * - ``rigid_body_mass_matrix``
     - Six-degree rigid-body mass/inertia matrix from the active profile.
   * - ``added_mass_matrix``
     - Hydrodynamic added-mass matrix.
   * - ``total_mass_matrix``
     - Runtime total mass matrix used for reporting and controller design.
   * - ``coriolis_matrix``
     - Fossen-style Coriolis/centripetal matrix computed from the body velocity.
   * - ``coriolis_force_torque_body``
     - Body-frame Coriolis force/torque vector.
   * - ``restoring_force_torque_body``
     - Body-frame restoring force/torque vector.
   * - ``restoring_torque_body``
     - Restoring torque slice used by attitude diagnostics.
   * - ``thruster_allocation_matrix``
     - Matrix mapping actuator directions and locations into body wrench terms.

Error behavior
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Error
     - Meaning
   * - ``OceanSimActionShapeError``
     - Raised by ``ActionSpace.validate`` for wrong vector lengths. The
       exception exposes ``error_code="invalid_action_shape"``.
   * - ``ValueError``
     - Raised by ``normalize_control_scheme`` for unknown control modes and by
       ``ActionSpace.validate`` for out-of-bounds values.
   * - ``TypeError``
     - Raised by ``AgentFactory.build_agent`` when the first argument is not an
       ``OceanSimClient`` or ``AUV`` instance.
   * - Protocol ``status="error"``
     - Returned by the simulator for unsupported actions, missing runtime
       objects, or invalid command payloads.

Runtime fields
--------------

The ``get_agents`` protocol response should be treated as a runtime state
envelope. The fields below are the documented contract for UI panels, Python
tools, replay metadata, and downstream controllers.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Meaning
   * - ``schema_version``
     - Runtime state schema version.
   * - ``id`` / ``agent_name``
     - Stable runtime identifier.
   * - ``agent_type`` / ``profile``
     - Agent role and profile name.
   * - ``shape`` / ``semantic_label`` / ``tags``
     - Visualization shape, semantic class, and grouping labels.
   * - ``position`` / ``pose.position`` / ``pose.rotation_rpy``
     - Runtime pose fields.
   * - ``pose.rotation_quat_xyzw``
     - Optional quaternion rotation, currently provided by the main AUV.
   * - ``velocity`` / ``angular_velocity``
     - Runtime velocity summary and optional body angular velocity.
   * - ``mode`` / ``speed``
     - Motion mode and scalar speed summary.
   * - ``size_m`` / ``proxy_auv``
     - Runtime footprint and whether the entry is a lightweight proxy.
   * - ``control_scheme`` / ``control_mode``
     - Active control contract.
   * - ``action_space`` / ``available_action_spaces``
     - Shape, fields, units, frame, optional bounds, and main AUV alternatives.
   * - ``sensors``
     - Sensor declarations or summaries.
   * - ``last_command`` / ``last_command_time`` / ``control_status``
     - Runtime diagnostics.
   * - ``controller_state``
     - Recordable waypoint/controller diagnostics, including error, integral,
       target, and saturation where available.
   * - ``depth_min`` / ``depth_max``
     - Optional proxy-agent depth limits.
   * - ``metadata``
     - Role, semantic label, tags, and experiment annotations.

Export trace contract
---------------------

``agent_timeline.jsonl`` rows include ``state``, ``command``,
``sensor_sequences``, and ``frame_trace`` so a dataset consumer can connect an
agent sample to the command that produced it, the sensor summary recorded with
it, and the world/base/sensor frames used by downstream tools.

Release checks
--------------

.. code-block:: powershell

   cd path\to\OceanSim\oceansim\python
   python tools\agents_schema_smoke.py
   python tools\scenario_agent_schema_smoke.py

.. code-block:: powershell

   cd path\to\OceanSim\oceansim
   godot --headless --path . --script res://tools/release_agent_runtime_smoke.gd
