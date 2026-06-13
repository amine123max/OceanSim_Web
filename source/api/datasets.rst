Dataset Tools
=============

Dataset tools convert live OceanSim runs into offline artifacts for mapping, evaluation, robotics integration, replay, and publication figures.

Recording
---------

.. py:class:: OceanSimPklRecorder

   Collect OceanSim frames into a pickle dataset for offline replay and figures.

   .. py:attribute:: scenario

      Scenario label stored in the dataset metadata.

   .. py:attribute:: voxel_size

      Point-cloud voxel size used when compacting frames.

   .. py:attribute:: max_points_per_frame

      Maximum number of points stored for each frame.

   .. py:method:: add_frame(state, point_cloud=None, dvl=None, imaging_sonar=None, lidar_2d=None, rgbd_dense=None, agents=None, planning=None, sim_time=None)

      Append one compact simulation frame.

   .. py:method:: to_dataset()

      Return a serializable dataset dictionary.

   .. py:method:: save(path)

      Write the dataset to a PKL file.

   .. py:method:: load(path)

      Load a PKL dataset dictionary.

.. py:function:: dataset_to_mapper(dataset, voxel_size=None)

   Build an ``OceanSimPointCloudMap`` from a PKL dataset, preserving trajectory and point-cloud frames.

.. py:function:: load_pkl_dataset(path)

   Load a PKL dataset through ``OceanSimPklRecorder.load``.

Replay
------

.. py:class:: OceanSimRunReplay

   Read an exported OceanSim run for deterministic offline inspection.

   .. py:method:: open(run_dir)

      Open an exported run directory.

   .. py:method:: frame_count()

      Return number of replay frames.

   .. py:method:: iter_frames()

      Iterate exported frame dictionaries.

   .. py:method:: trajectory()

      Return trajectory as a NumPy array.

   .. py:method:: sensor_frames(sensor_name)

      Iterate frames for one sensor.

   .. py:method:: summary()

      Return high-level run metadata.

   .. py:method:: tum_trajectory_rows()

      Export trajectory rows for TUM-style benchmark tools.

   .. py:method:: euroc_trajectory_rows()

      Export trajectory rows for EuRoC-style benchmark tools.

Camera images
-------------

.. list-table::
   :header-rows: 1
   :widths: 42 58

   * - Function
     - Description
   * - ``camera_payload_to_arrays(payload)``
     - Convert an OceanSim camera payload to RGB, depth, and segmentation arrays.
   * - ``save_camera_payload(payload, output_dir, prefix="camera")``
     - Save camera payload arrays as PNG files.
   * - ``AUV.save_camera_images(output_dir, prefix="camera")``
     - Fetch current camera payload and save images in one call.

Robotics exports
----------------

.. list-table::
   :header-rows: 1
   :widths: 42 58

   * - Function
     - Description
   * - ``export_ros2_bridge_dataset(run_dir, output_dir=None)``
     - Write ROS2-bridge-friendly JSONL topics from an exported OceanSim run.
   * - ``export_mcap_like_dataset(run_dir, output_dir=None)``
     - Write an MCAP-ready sidecar dataset without requiring the MCAP Python package.
   * - ``reconstruct_mesh_obj(dataset_path, output_obj, ...)``
     - Reconstruct an OBJ mesh from an OceanSim point-cloud PKL dataset.
