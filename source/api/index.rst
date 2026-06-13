API Documentation
=================

This section documents the public OceanSim integration surface. It follows the same pattern used by Sphinx API pages: summary tables first, then detailed class, function, method, parameter, and return descriptions.

Modules
-------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Module
     - Contents
   * - :doc:`protocol`
     - Wire format, request/response envelopes, action catalog, errors, and batch requests.
   * - :doc:`client`
     - Low-level TCP client, request IDs, connection lifecycle, exceptions, and command helpers.
   * - :doc:`auv`
     - High-level AUV wrapper, state object, force controls, sensors, maps, agents, navigation overlays, and RL step loop.
   * - :doc:`agents`
     - Agent definitions, action spaces, control schemes, and runtime agent wrappers.
   * - :doc:`sensors`
     - Payload normalization, validation, required fields, point cloud access, and sensor family conventions.
   * - :doc:`mapping`
     - Coordinate conversion, point cloud processing, OceanSim map figures, RGB-D dense mapping, and adapters.
   * - :doc:`datasets`
     - PKL recording, replay, camera image export, robotics exports, MCAP-like sidecars, and mesh reconstruction.

Public exports
--------------

.. list-table::
   :header-rows: 1
   :widths: 32 28 40

   * - Symbol
     - Defined in
     - Role
   * - ``OceanSimClient``
     - ``client.py``
     - Low-level TCP transport and response handling.
   * - ``AUV``, ``AUVState``
     - ``auv_interface.py``
     - High-level control and state access wrappers.
   * - ``AgentDefinition``, ``AgentFactory``, ``OceanSimAgent``
     - ``agents.py``
     - Typed agent definitions and runtime action dispatch.
   * - ``validate_sensor_payload``
     - ``sensor_schema.py``
     - Professional sensor envelope validation.
   * - ``xyz_from_cloud``
     - ``point_cloud.py``
     - Convert OceanSim point-cloud payloads to NumPy arrays.
   * - ``OceanSimPointCloudMap``
     - ``pointcloud_mapping.py``
     - Accumulate and render point-cloud maps.
   * - ``RGBDPointCloudSLAM``
     - ``rgbd_slam.py``
     - Lightweight RGB-D dense point-cloud accumulator.
   * - ``OceanSimPklRecorder``
     - ``recording.py``
     - Collect frame data into offline PKL datasets.
   * - ``OceanSimRunReplay``
     - ``replay.py``
     - Read exported runs and iterate replay data.
