Mapping Utilities
=================

Mapping utilities convert coordinates, process point clouds, accumulate maps, render figures, and adapt robotics payloads into OceanSim schema conventions.

Coordinates
-----------

.. list-table::
   :header-rows: 1
   :widths: 42 58

   * - Function
     - Description
   * - ``godot_to_oceansim(value)``
     - Convert Godot XYZ to OceanSim user XYZ: ``[X, -Z, Y]``.
   * - ``oceansim_to_godot(value)``
     - Convert OceanSim user XYZ to Godot XYZ: ``[x, z, -y]``.
   * - ``oceansim_to_ros_enu(value)``
     - Return an ENU-compatible OceanSim vector.
   * - ``oceansim_to_ros_ned(value)``
     - Convert OceanSim ENU to ROS NED: ``[y, x, -z]``.
   * - ``state_position_godot(state)``
     - Extract and convert a state dictionary position to Godot coordinates.

OceanSim point-cloud map
------------------------

.. py:class:: OceanSimPointCloudMap

   Accumulates OceanSim point clouds and renders research map figures.

   .. py:method:: add_cloud(cloud, world=True, min_range=0.0, max_range=inf, pose=None)

      Add one OceanSim cloud to the map.

   .. py:method:: add_pose(position)

      Append one trajectory point.

   .. py:method:: cloud_array()

      Return all accumulated points as a NumPy array.

   .. py:method:: save_npz(path)

      Persist map arrays to a compressed NumPy file.

   .. py:method:: load_npz(path)

      Reload a previously saved map.

   .. py:method:: render_colored_map(output_path, plane="xz", color_by="height", title=None, dark=True, point_size=1.0, trajectory_width=2.2, dpi=220)

      Render a dense colored point-cloud map.

   .. py:method:: render_exploration_map(output_path, plane="xz", title=None, point_size=0.45, dpi=220)

      Render a white-background sparse exploration map.

RGB-D SLAM
----------

.. py:class:: RGBDPointCloudSLAM

   Lightweight dense point-cloud accumulator for RGB-D frames.

   .. py:method:: add_frame(rgbd, pose=None, force_keyframe=False)

      Add a keyframe or dense RGB-D frame.

   .. py:method:: point_array()

      Return fused point coordinates.

   .. py:method:: color_array()

      Return fused RGB colors.

   .. py:method:: fused_arrays()

      Return ``(points, colors)`` arrays.

   .. py:method:: save_ply(path)

      Export a colored PLY point cloud.

   .. py:method:: save_npz(path)

      Persist dense mapping arrays.

   .. py:method:: render(path, width=1280, height=860, color_mode="range")

      Render a dense map figure.

Adapters
--------

.. list-table::
   :header-rows: 1
   :widths: 44 56

   * - Function
     - Purpose
   * - ``make_structured_cloud_from_xyz(points, ...)``
     - Build OceanSim structured cloud format from external xyz-like outputs.
   * - ``raycast_lidar_to_oceansim_cloud(lidar_output, ...)``
     - Normalize raycast or semantic lidar output.
   * - ``ros_pointcloud2_like_to_oceansim_cloud(msg_or_dict, ...)``
     - Normalize decoded ROS PointCloud2-like data.
   * - ``sonar_image_to_oceansim_sonar(image, ...)``
     - Normalize FLS/MSIS/multibeam image data.
   * - ``dvl_to_oceansim_dvl(raw, ...)``
     - Normalize DVL-like outputs from external tools.
