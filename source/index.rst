OceanSim
========

.. raw:: html

   <div class="oceansim-title-card">
     <img src="img/OceanSim_Title.png" alt="OceanSim" />
   </div>

OceanSim is a research-oriented underwater robotics simulation environment built on Godot. It provides a controllable AUV runtime, configurable marine scenarios, onboard sensor simulation, an external TCP control protocol, and a Python SDK for automated experiments, mapping, dataset export, and replay.

The documentation is organized as a tool manual: start with installation and workflows, then use the API reference for protocol messages, Python clients, AUV control, sensor payloads, mapping utilities, and dataset tools.

Features
--------

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Area
     - Capabilities
   * - Simulation runtime
     - Godot 4.5 project, AUV body, water physics, ocean current, terrain, static obstacles, dynamic agents, and simulator UI.
   * - External control
     - Line-delimited JSON TCP protocol with request IDs, structured response envelopes, state polling, stepping, simulation control, and batch requests.
   * - Sensors
     - Depth, IMU, DVL, camera, RGB-D dense point cloud, 2D/3D lidar, imaging sonar, multibeam sonar, and side-scan sonar payloads.
   * - Python SDK
     - Connection management, AUV wrapper, coordinate conversion, sensor schema validation, point-cloud conversion, mapping, recording, replay, and robotics exports.

Documentation map
-----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Page
     - Purpose
   * - :doc:`guide/getting-started`
     - Prepare Godot, install the Python SDK, and run the first TCP connection check.
   * - :doc:`guide/using-oceansim`
     - Understand runtime concepts, coordinate frames, LLM/MPC navigation, RL step loops, and dataset capture workflows.
   * - :doc:`api/protocol`
     - Detailed request envelopes, response envelopes, actions, payloads, errors, and batch semantics.
   * - :doc:`api/client`
     - Low-level Python TCP client, exceptions, connection lifecycle, and request helpers.
   * - :doc:`api/auv`
     - High-level AUV state, force control, sensors, maps, agents, navigation overlays, and Gym-style step API.
   * - :doc:`api/sensors`
     - Professional sensor payload envelope, validation helpers, required fields, and payload families.
   * - :doc:`api/datasets`
     - Recording, replay, camera image export, robotics export sidecars, MCAP-ready metadata, and mesh reconstruction.

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   guide/getting-started
   guide/using-oceansim
   guide/agents
   guide/scenarios
   guide/sensors

.. toctree::
   :maxdepth: 3
   :caption: API Documentation

   api/index
   api/protocol
   api/client
   api/auv
   api/agents
   api/sensors
   api/mapping
   api/datasets

.. toctree::
   :maxdepth: 2
   :caption: Developer Guide

   developer/index
   developer/troubleshooting
   developer/license
