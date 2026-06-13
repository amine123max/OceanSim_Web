Scenarios
=========

Scenario JSON files keep map size, terrain profile, obstacle definitions, benchmark seeds, semantic tags, and recommended vehicle settings outside runtime code.

Scenario files
--------------

.. list-table::
   :header-rows: 1
   :widths: 28 30 42

   * - File
     - Use case
     - Notes
   * - ``Static_Map.json``
     - Static obstacle navigation
     - Baseline map for planning, sensing checks, and deterministic experiments.
   * - ``Dynamic_Map.json``
     - Dynamic interaction
     - Useful for moving-agent and obstacle-avoidance experiments.
   * - ``NarrowMap.json``
     - Narrow passage mapping
     - Canyon-like traversal and local mapping.
   * - ``PaleMap.json``
     - Alternative map profile
     - Visual and navigation variation for regression checks.

Map actions
-----------

.. list-table::
   :header-rows: 1
   :widths: 28 35 37

   * - Action
     - Payload
     - Result
   * - ``set_scenario``
     - ``{scenario, seed}``
     - Regenerates the map by scenario name.
   * - ``generate_map``
     - ``{scenario?, seed?}``
     - Generates a named or default procedural terrain.
   * - ``get_map_info``
     - ``{}``
     - Returns dimensions, path points, scenario name, and map metadata.
   * - ``get_terrain_grid``
     - ``{cell_size, inflation_radius, include_static_obstacles, include_dynamic_agents}``
     - Returns occupancy and class grids for planners.

Dynamic agents
--------------

Dynamic AUV-like agents are managed separately from static obstacle geometry so planners can distinguish fixed map structure from moving targets.

.. list-table::
   :header-rows: 1
   :widths: 36 64

   * - API
     - Purpose
   * - ``spawn_agent(config)``
     - Create a dynamic proxy AUV or obstacle agent.
   * - ``move_agent(id, position)``
     - Teleport or reposition an existing dynamic agent.
   * - ``set_agent_velocity(id, velocity)``
     - Drive a proxy agent with an external velocity vector.
   * - ``configure_acoustic_comm(...)``
     - Configure underwater communication latency, bandwidth, range, and packet drop rate.

Agent schema fields
-------------------

Every scenario declares an ``agents`` array. The main AUV entry is metadata for
the physical vehicle already present in the scene; non-main entries can be
spawned by the scenario loader.

.. list-table::
   :header-rows: 1
   :widths: 32 68

   * - Field
     - Purpose
   * - ``schema_version``
     - Version of the agent definition format.
   * - ``agent_name``
     - Stable runtime identifier such as ``auv/main`` or ``target_01``.
   * - ``agent_type``
     - Logical role such as ``main_auv`` or ``proxy_auv``.
   * - ``is_main_agent``
     - ``true`` for the scene-owned physical AUV; ``false`` for dynamic proxy agents.
   * - ``profile``
     - Vehicle profile or runtime profile name.
   * - ``location`` / ``rotation``
     - Initial pose fields.
   * - ``control_scheme``
     - One of ``force_3d``, ``body_force_3d``, ``thrusters``,
       ``external_velocity``, ``waypoint_pid``, ``body_wrench_6dof``,
       ``body_velocity_6dof``, or ``custom_dynamics_6dof``.
   * - ``sensors``
     - Sensor names or sensor declaration dictionaries.
   * - ``metadata``
     - Role, semantic label, tags, and experiment-specific annotations.
