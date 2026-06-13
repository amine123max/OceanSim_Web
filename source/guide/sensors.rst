Sensors
=======

OceanSim sensor modules output structured payloads for the TCP protocol, Python SDK, recorders, replay tools, and visualization utilities.

Sensor families
---------------

.. list-table::
   :header-rows: 1
   :widths: 20 34 46

   * - Family
     - Modules
     - Typical output
   * - Navigation
     - Depth, IMU, DVL
     - Depth, acceleration, angular velocity, local/world velocity, and altitude-like velocity cues.
   * - Vision
     - Camera, RGB-D dense sensor
     - RGB frames, depth maps, segmentation-like payloads, camera intrinsics, and RGB-D clouds.
   * - Range
     - 2D lidar, 3D lidar
     - 2D scans, structured point clouds, organized range images, ring/column metadata, and intensity.
   * - Sonar
     - Imaging, multibeam, side-scan
     - Acoustic-style beams, range bins, intensity images, and mapping observations.

Payload envelope
----------------

Every professional sensor payload is normalized to an ``oceansim_sensor_payload`` envelope. Sensor-specific fields are preserved, and the common envelope provides stable metadata for downstream tools.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Field
     - Meaning
   * - ``schema_name`` / ``schema_version``
     - Identifies the OceanSim payload schema and version.
   * - ``sensor_type``
     - Human-readable sensor family, such as ``lidar_3d`` or ``dvl``.
   * - ``sim_time``, ``timestamp_sim``, ``timestamp_wall``
     - Simulation and wall-clock timing values.
   * - ``frame_id``, ``sensor_frame_id``, ``parent_frame_id``
     - Coordinate-frame metadata for robot and sensor transforms.
   * - ``extrinsic_xyz_rpy``, ``extrinsic_quat_xyzw``
     - Sensor extrinsics in Euler and quaternion forms.
   * - ``covariance``
     - Optional uncertainty metadata using a diagonal-variance convention.

Data access
-----------

.. code-block:: python

   from oceansim_client import AUV, xyz_from_cloud

   with AUV() as auv:
       sensors = auv.get_sensors(validate=True)
       cloud = auv.get_point_cloud_3d()
       points = xyz_from_cloud(cloud, world=True)
