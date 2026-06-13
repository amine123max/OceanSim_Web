Development Notes
=================

Repository layout
-----------------

.. list-table::
   :header-rows: 1
   :widths: 34 66

   * - Path
     - Purpose
   * - ``assets/models/``
     - AUV and USV model resources.
   * - ``assets/images/branding/``
     - Branding assets and application icons.
   * - ``scenes/``
     - Godot scene files and simulator entry points.
   * - ``scripts/auv/``
     - AUV body, thrusters, and buoyancy scripts.
   * - ``scripts/sensors/``
     - Sensor modules for navigation, vision, range, and sonar payloads.
   * - ``scripts/network/``
     - TCP server and protocol envelope helpers.
   * - ``python/oceansim_client/``
     - Python SDK, mapping helpers, sensor schema, and dataset tools.
   * - ``vehicle_profiles/``
     - AUV physical configuration and thruster profile definitions.

Change guidelines
-----------------

* When moving Godot resources, update both scene files and script-level ``res://`` paths.
* Treat the TCP protocol and Python SDK as public integration surfaces for external controllers.
* Keep generated datasets, exports, caches, and package artifacts outside committed source folders.
* When changing sensor fields, update Godot emitters, Python schema validation, and dataset/replay readers together.

Smoke tests
-----------

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Test area
     - Representative files
   * - Protocol
     - ``tools/protocol_envelope_smoke.gd``, ``python/tools/tcp_api_smoke.py``
   * - Agents
     - ``scripts/agents/agent_manager.gd``, ``tools/scenario_agent_schema_smoke.gd``, ``python/tools/agents_schema_smoke.py``, ``python/tools/scenario_agent_schema_smoke.py``
   * - Sensors
     - ``tools/sensor_schema_smoke.gd``, ``python/tools/sensor_schema_smoke.py``
   * - AUV physics
     - ``tools/auv_physics_smoke.gd``, ``tools/auv_six_dof_smoke.gd``, ``tools/fossen_dynamics_smoke.gd``, ``tools/vehicle_profile_smoke.gd``
   * - Datasets
     - ``tools/export_dataset_smoke.gd``, ``python/tools/replay_dataset_smoke.py``
   * - Mapping/export
     - ``python/tools/export_pointcloud_formats_smoke.py``, ``python/tools/robotics_exports_smoke.py``

Release gate
------------

Before publishing a branch or preparing a release artifact, run the focused
checks for the files you changed. For agent and scenario work:

The current agent release gate explicitly includes ``release_agent_runtime_smoke.gd``.
The Windows executable gate uses ``release_exe_smoke.py`` after exporting the
release binary.

.. code-block:: powershell

   cd path\to\OceanSim\oceansim\python
   python -m compileall oceansim_client tools
   python tools\agents_schema_smoke.py
   python tools\scenario_agent_schema_smoke.py

.. code-block:: powershell

   cd path\to\OceanSim\oceansim
   godot --headless --path . --script res://tools/scenario_agent_schema_smoke.gd
   godot --headless --path . --script res://tools/scenario_config_smoke.gd
   godot --headless --path . --script res://tools/professional_sim_audit.gd
   godot --headless --path . --script res://tools/fossen_dynamics_smoke.gd
   godot --headless --path . --script res://tools/vehicle_profile_smoke.gd
   godot --headless --path . --script res://tools/release_agent_runtime_smoke.gd

For Windows executable artifacts:

.. code-block:: powershell

   cd path\to\OceanSim\oceansim
   godot --headless --path . --export-release "Windows Desktop" "../dist/OceanSim.exe"
   cd path\to\OceanSim
   python oceansim\python\tools\release_exe_smoke.py --exe dist\OceanSim.exe --startup-timeout 60

For documentation changes:

.. code-block:: powershell

   cd path\to\OceanSim_Web
   python scripts\build_docs.py
