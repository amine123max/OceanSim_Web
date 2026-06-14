Sensor Schema
=============

The ``sensor_schema`` module defines OceanSim's professional sensor envelope. It preserves sensor-specific payload fields while adding stable metadata required by downstream robotics, mapping, dataset, and replay tools.

Schema fields
-------------

.. list-table::
   :header-rows: 1
   :widths: 34 18 48

   * - Field
     - Required
     - Description
   * - ``enabled``
     - yes
     - Whether the sensor is enabled.
   * - ``status``
     - yes
     - Status string, usually ``ok`` or ``disabled``.
   * - ``schema_name``
     - yes
     - Must be ``oceansim_sensor_payload``.
   * - ``schema_version``
     - yes
     - Current minimum schema version is ``2``.
   * - ``sensor_type``
     - yes
     - Sensor family name.
   * - ``sim_time``, ``timestamp_sim``, ``timestamp_wall``, ``timestamp``
     - yes
     - Timing metadata.
   * - ``sequence``
     - yes
     - Frame or scan sequence number.
   * - ``frame_id``, ``sensor_frame_id``, ``parent_frame_id``
     - yes
     - Coordinate-frame metadata.
   * - ``noise_seed``
     - yes
     - Deterministic seed used for noise metadata.
   * - ``extrinsic_xyz_rpy``, ``extrinsic_quat_xyzw``
     - yes
     - Sensor extrinsics.
   * - ``covariance``
     - yes
     - Uncertainty metadata mapping.

Functions
---------

.. py:function:: normalize_sensor_payload(payload, sensor_type="unknown")

   Return a copy of a sensor payload with missing envelope fields filled in. This is tolerant for compact payloads that do not yet include the full envelope.

   :returns: normalized payload dictionary.

.. py:function:: validate_sensor_payload(payload, name="sensor")

   Normalize then validate the payload. It checks required fields, schema name/version, timestamps, frame identifiers, extrinsic vector lengths, and covariance shape.

   :raises SensorSchemaError: when validation fails.

.. py:function:: validate_sensor_set(sensors, required=())

   Validate every payload in a sensor dictionary and optionally check that required sensor keys are present.

   :returns: normalized payloads keyed by sensor name.

Point-cloud access
------------------

3D lidar and RGB-D modules expose structured cloud payloads. Use ``point_cloud.py`` helpers instead of manual list indexing.

.. list-table::
   :header-rows: 1
   :widths: 38 62

   * - Function
     - Purpose
   * - ``structured_cloud_to_numpy(cloud, fields=None)``
     - Convert ``point_cloud`` records to a dense NumPy array.
   * - ``xyz_from_cloud(cloud, world=False)``
     - Return local or world Nx3 coordinates from structured or compact payloads.
   * - ``intensity_from_cloud(cloud)``
     - Return per-point intensity or zeros for compact xyz-only clouds.
   * - ``organized_range_image(cloud)``
     - Return an organized range image as ``[rings, columns]``.
   * - ``filter_by_range(points, min_range=0.0, max_range=inf)``
     - Filter point arrays by Euclidean range.
