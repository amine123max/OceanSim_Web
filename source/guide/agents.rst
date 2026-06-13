Agents and Runtime
==================

OceanSim agents are runtime-controlled participants in a marine scenario. The
main AUV is a physical vehicle with thrusters, buoyancy, hydrodynamic terms, and
onboard sensors. Dynamic proxy agents are lightweight moving participants used
for obstacle-avoidance, communication, tracking, and multi-target experiments.

The goal is to keep experiment setup explicit: scenario files describe the map,
vehicle roles, initial placement, motion policy, and sensor expectations; Python
code controls the run through typed wrappers and protocol actions.

Agent roles
-----------

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Role
     - Description
   * - ``main_auv``
     - The controllable physical AUV. It owns the primary state, sensors, force
       control, thruster control, dataset export hooks, and navigation overlays.
   * - ``proxy_auv``
     - A lightweight dynamic participant. It can move autonomously or accept an
       external velocity command and is included in occupancy grids and agent
       summaries.
   * - ``static_obstacle``
     - Non-moving map geometry managed by the obstacle system rather than the
       agent system.

Control contracts
-----------------

OceanSim documents each control mode as an action contract. The contract names
the vector fields, units, and coordinate frame so controllers, RL policies, and
dataset replays can be compared without reading simulator internals.

.. list-table::
   :header-rows: 1
   :widths: 26 26 48

   * - Control scheme
     - Action vector
     - Use
   * - ``force_3d``
     - ``[fx, fy, fz]`` in Newtons
     - Main AUV force control through the world-frame ``set_force_world`` entry.
   * - ``body_force_3d``
     - ``[fx, fy, fz]`` in Newtons
     - Main AUV force control through the body-frame ``set_force_body`` entry.
   * - ``thrusters``
     - ``[thruster_0, thruster_1, thruster_2, thruster_3, thruster_4, thruster_5]``
     - Direct actuator experiments using vehicle-profile ordering.
   * - ``external_velocity``
     - ``[vx, vy, vz]`` in m/s
     - Proxy AUV motion in the Godot world frame.
   * - ``waypoint_pid``
     - ``[world_x, world_z, depth]``
     - High-level target tracking through Python control utilities.
   * - ``body_wrench_6dof``
     - ``[fx, fy, fz, tx, ty, tz]``
     - Body-frame force/torque contract for six-degree controller research.
   * - ``body_velocity_6dof``
     - ``[u, v, w, p, q, r]``
     - Body-frame linear/angular velocity contract.
   * - ``custom_dynamics_6dof``
     - ``[lin_ax, lin_ay, lin_az, ang_ax, ang_ay, ang_az]``
     - Reserved for model-driven six-degree dynamics research.

Python example
--------------

.. code-block:: python

   from oceansim_client import AUV, AgentDefinition, AgentFactory

   with AUV() as auv:
       main = AgentFactory.build_agent(
           auv,
           AgentDefinition(agent_name="auv/main", control_scheme="force_3d"),
           spawn=False,
       )
       main.act([0.0, 120.0, 0.0])

       target = AgentFactory.build_agent(
           auv,
           {
               "agent_name": "target_01",
               "agent_type": "proxy_auv",
               "is_main_agent": False,
               "location": [4.0, -7.0, 6.0],
               "control_scheme": "external_velocity",
               "metadata": {"role": "moving_target"},
           },
       )
       target.act([0.2, 0.0, -0.1])

Scenario definition
-------------------

Scenario files keep agent configuration explicit and versioned. Every public
scenario declares the main AUV in an ``agents`` array; dynamic proxy agents can
be added with the same shape and are spawned by the scenario loader when
``is_main_agent`` is false.

.. code-block:: json

   {
     "schema_version": 1,
     "id": "Dynamic_Map",
     "display_name": "Dynamic Obstacle Benchmark Field",
     "generator": "benchmark_dynamic_field",
     "map_size_m": [40.0, 40.0],
     "agents": [
       {
         "schema_version": 1,
         "agent_name": "auv/main",
         "agent_type": "main_auv",
         "is_main_agent": true,
         "profile": "oceansim_torpedo_auv",
         "location": [0.0, -6.0, -17.0],
         "rotation": [0.0, 0.0, 0.0],
         "control_scheme": "force_3d",
         "sensors": [
           "depth",
           "imu",
           "dvl",
           "camera",
           "rgbd_dense_cloud",
           "lidar_2d",
           "lidar_3d",
           "imaging_sonar",
           "multibeam_sonar",
           "side_scan_sonar"
         ],
         "metadata": {
           "role": "ego_vehicle",
           "semantic_label": "auv",
           "tags": ["main", "controlled", "dynamic_benchmark"]
         }
       },
       {
         "schema_version": 1,
         "agent_name": "target_01",
         "agent_type": "proxy_auv",
         "is_main_agent": false,
         "location": [4.0, -7.0, 6.0],
         "rotation": [0.0, 0.0, 0.0],
         "control_scheme": "external_velocity",
         "metadata": {
           "role": "moving_target",
           "semantic_label": "auv",
           "tags": ["dynamic", "vehicle"]
         }
       }
     ]
   }

Scenario agent fields
---------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Meaning
   * - ``schema_version``
     - Version of the agent definition format.
   * - ``agent_name``
     - Stable runtime identifier, for example ``auv/main`` or ``target_01``.
   * - ``agent_type``
     - Logical role such as ``main_auv`` or ``proxy_auv``.
   * - ``is_main_agent``
     - ``true`` for the scene-owned physical AUV; ``false`` for spawned proxy agents.
   * - ``profile``
     - Vehicle or runtime profile name.
   * - ``location`` / ``rotation``
     - Initial pose fields in Godot-world coordinates and degrees.
   * - ``control_scheme``
     - Action contract used by the agent.
   * - ``sensors``
     - Sensor names or typed sensor declaration dictionaries.
   * - ``metadata``
     - Role, semantic label, tags, and experiment annotations.

Runtime state fields
--------------------

``get_agents`` exposes a versioned runtime summary. Dynamic proxy agents are
reported by the agent manager; the main AUV can be represented with the same
field names for replay and dataset tooling.

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
     - Logical role and vehicle/runtime profile.
   * - ``shape`` / ``semantic_label`` / ``tags``
     - Visualization shape, semantic class, and grouping labels.
   * - ``position`` / ``pose.position`` / ``pose.rotation_rpy``
     - Runtime pose in the simulator frame.
   * - ``pose.rotation_quat_xyzw``
     - Optional quaternion rotation, currently provided by the main AUV.
   * - ``velocity`` / ``angular_velocity``
     - Linear velocity summary and optional body angular velocity.
   * - ``mode`` / ``speed``
     - Motion mode and scalar speed summary.
   * - ``size_m`` / ``proxy_auv``
     - Runtime footprint and whether the entry is a lightweight proxy.
   * - ``control_scheme`` / ``control_mode``
     - Active control contract.
   * - ``action_space`` / ``available_action_spaces``
     - Machine-readable shape, fields, units, frame, optional bounds, and main
       AUV alternatives.
   * - ``sensors``
     - Sensor declarations or sensor summaries associated with the agent.
   * - ``last_command`` / ``last_command_time`` / ``control_status``
     - Runtime diagnostics for replay and debugging.
   * - ``controller_state``
     - Recordable controller diagnostics such as waypoint error, integral,
       target, and saturation flags.
   * - ``depth_min`` / ``depth_max``
     - Optional proxy-agent depth limits.
   * - ``metadata``
     - Role, tags, semantic label, and experiment-specific annotations.

Export trace fields
-------------------

``agent_timeline.jsonl`` links each agent sample to the frame-level state,
command, sensor summary, and frame identifiers used by replay tools.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Meaning
   * - ``state``
     - Full agent state snapshot for that timeline row.
   * - ``command``
     - Last recorded command envelope, including the command frame when present.
   * - ``sensor_sequences``
     - Per-agent sensor declarations or main-AUV sensor sequence summaries.
   * - ``frame_trace``
     - ``world_frame``, ``base_frame``, ``sensor_frames``, and ``command_frame``
       used to connect data exports back to the runtime agent.

Multi-agent workflow
--------------------

The recommended workflow keeps configuration, launch, control, recording, and
replay separated:

1. Configure the scenario JSON with the main AUV and any proxy agents needed by
   the experiment.
2. Start OceanSim and select the scenario through ``set_scenario`` or the UI.
3. Use ``AgentFactory.build_agent`` for typed Python bindings.
4. Send actions through ``OceanSimAgent.act`` so vector length and bounds are
   checked before TCP dispatch.
5. Record the run with the dataset tools when sensor payloads, commands, and
   replay metadata are needed.
6. Re-open the export with ``OceanSimRunReplay`` for offline inspection.

Recommended release checks
--------------------------

- Verify that ``get_agents`` returns every dynamic agent with position, mode,
  size, role metadata, action space, and control scheme.
- Verify that each documented action vector is accepted or rejected according to
  its ``ActionSpace``.
- Verify that ``python tools\scenario_agent_schema_smoke.py`` accepts every
  scenario JSON file.
- Verify that dynamic agents appear in occupancy grids when
  ``include_dynamic_agents`` is enabled.
- Verify that acoustic communication tests cover latency, range, bandwidth, and
  packet-drop settings.
