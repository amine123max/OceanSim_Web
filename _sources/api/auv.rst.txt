AUV Interface
=============

The ``AUV`` wrapper provides a research-friendly API on top of ``OceanSimClient``. It hides raw protocol envelopes for common state, control, sensor, map, agent, overlay, dataset, and Gym-style workflows.

AUVState
--------

.. py:class:: AUVState(data)

   Typed view of an OceanSim state dictionary.

   .. list-table::
      :header-rows: 1
      :widths: 32 68

      * - Attribute
        - Meaning
      * - ``position``
        - OceanSim / ROS ENU position as a NumPy vector.
      * - ``position_godot_xyz``
        - Converted Godot world position.
      * - ``position_ros_enu``, ``position_ros_ned``
        - ROS-compatible frame conversions.
      * - ``velocity``
        - OceanSim velocity vector.
      * - ``depth``, ``speed``, ``heading``
        - Scalar navigation values.
      * - ``lidar_2d``, ``lidar_3d``, ``dvl``, ``camera``
        - Embedded sensor payloads from the state response.

   .. py:property:: x

      X coordinate in OceanSim user frame.

   .. py:property:: y

      Y coordinate in OceanSim user frame.

   .. py:property:: z

      Z coordinate in OceanSim user frame.

AUV
---

.. py:class:: AUV(host="localhost", port=9876, auto_launch=False, exe_path=None, timeout=5.0)

   High-level AUV controller and data access object.

   :param str host: simulator hostname.
   :param int port: simulator TCP port.
   :param bool auto_launch: launch a packaged executable before connecting.
   :param str exe_path: optional packaged simulator executable path.
   :param float timeout: response timeout in seconds.

Connection
~~~~~~~~~~

.. py:method:: AUV.connect(**kwargs)

   Connect to the simulator. Extra keyword arguments are forwarded to ``OceanSimClient.connect``.

.. py:method:: AUV.disconnect()

   Disconnect the underlying TCP client.

Control
~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 38 62

   * - Method
     - Description
   * - ``set_force(fx, fy, fz=0.0)``
     - Compatibility alias for world-frame force control.
   * - ``set_force_world(fx, fy, fz=0.0)``
     - Apply force in OceanSim world/user coordinates.
   * - ``set_force_body(fx, fy, fz=0.0)``
     - Apply force in the AUV body frame.
   * - ``set_body_wrench(fx, fy, fz, tx, ty, tz)``
     - Apply body-frame force and torque.
   * - ``set_body_velocity(u, v, w, p, q, r)``
     - Set body-frame linear and angular velocity targets.
   * - ``surge(power=100.0)``
     - Move forward using a positive y force.
   * - ``strafe(power=100.0)``
     - Move laterally using an x force.
   * - ``heave(power=100.0)``
     - Move vertically using a z force.
   * - ``stop()``
     - Apply a zero force.
   * - ``set_pose(position, rotation_deg=None, yaw_deg=None)``
     - Reset AUV pose and clear velocities.
   * - ``hold_depth_step(...)``
     - One PD depth-hold control step.
   * - ``hold_heading_step(...)``
     - One heading correction step.
   * - ``track_waypoint_step(...)``
     - One force-control waypoint tracking step.
   * - ``step(action)``
     - Gym-style step returning observation, reward, done, and info.

.. py:method:: AUV.set_force(fx, fy, fz=0.0)

   Compatibility alias for ``set_force_world`` with force vector
   ``[fx, fy, fz]``. Use this for MPC, scripted navigation, and
   continuous-control experiments that operate in the world frame.

   :returns: raw protocol response dictionary.

.. py:method:: AUV.set_force_world(fx, fy, fz=0.0)

   Send ``set_force_world`` with a world-frame force vector.

.. py:method:: AUV.set_force_body(fx, fy, fz=0.0)

   Send ``set_force_body`` with a body-frame force vector.

.. py:method:: AUV.set_body_wrench(fx, fy, fz, tx, ty, tz)

   Send ``set_body_wrench`` with body-frame force and torque.

.. py:method:: AUV.set_body_velocity(u, v, w, p, q, r)

   Send ``set_body_velocity`` with body-frame linear and angular velocity
   components.

.. py:method:: AUV.hold_depth_step(target_depth, forward_force=0.0, kp=70.0, kd=25.0, max_vertical_force=180.0)

   Read current state, compute a bounded vertical force from depth error and depth rate, send force control, and annotate the response with control diagnostics.

.. py:method:: AUV.track_waypoint_step(world_x, world_z, nav_depth=None, force_power=120.0, depth_power=60.0, arrival_dist=1.0)

   Compute one normalized force command toward a Godot X/Z map-plane waypoint.
   The returned protocol response includes a ``control`` dictionary with
   ``mode="waypoint_pid"``, ``error``, ``integral``, ``saturation``, ``target``,
   ``force``, and ``dt``.

   :returns: ``(arrived, response)``.

State and sensors
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 38 62

   * - Method
     - Sensor or state
   * - ``get_state()``
     - Current ``AUVState``.
   * - ``get_lidar_2d()``
     - 2D planar scan payload.
   * - ``get_lidar_3d()`` / ``get_point_cloud_3d()``
     - Structured 3D lidar point cloud.
   * - ``get_dvl()``
     - Doppler velocity log payload.
   * - ``get_imaging_sonar()``
     - Forward-looking imaging sonar payload.
   * - ``get_multibeam_sonar()``
     - Multibeam sonar payload.
   * - ``get_side_scan_sonar()``
     - Side-scan sonar payload.
   * - ``get_rgbd_dense_cloud()``
     - RGB-D dense point-cloud payload.
   * - ``get_camera()``
     - Camera RGB/depth/segmentation-like payload from latest state.
   * - ``get_sensors(validate=True)``
     - Full sensor dictionary with schema validation by default.

.. py:method:: AUV.get_sensors(validate=True)

   Request all active sensors and validate every payload through ``validate_sensor_set`` unless validation is disabled.

   :returns: ``Dict[str, Dict[str, Any]]`` keyed by sensor name.

Maps, agents, and overlays
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Method
     - Description
   * - ``set_scenario(scenario, seed=0)``
     - Load a named map scenario.
   * - ``get_map_info()``
     - Return terrain and scenario metadata.
   * - ``get_terrain_grid(...)``
     - Return 2D occupancy grid for planners.
   * - ``spawn_obstacle(config)``
     - Create a static obstacle.
   * - ``spawn_agent(config)``
     - Create a dynamic AUV-like agent.
   * - ``set_agent_velocity(id, velocity)``
     - Externally drive a proxy agent.
   * - ``send_acoustic_message(sender_id, receiver_id, payload)``
     - Queue a simulated acoustic message.
   * - ``set_nav_path(path)``
     - Display a planned path on the 2D/3D map overlays.
   * - ``set_waypoint(world_x, world_z)``
     - Display one target waypoint.
   * - ``set_pred_trajectory(points)``
     - Display a predicted trajectory such as an MPC horizon.
   * - ``clear_nav()``
     - Clear all overlay planning graphics.
