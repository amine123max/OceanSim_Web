Troubleshooting
===============

Common issues
-------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Symptom
     - Recommended check
   * - Python client cannot connect
     - Confirm the Godot simulator is running and TCP port ``9876`` is available.
   * - Command times out
     - Increase timeout for export-heavy commands and verify the simulator main scene is not paused.
   * - Protocol error returned
     - Inspect ``type``, ``action``, ``data``, and ``protocol_version`` fields.
   * - Godot reports missing resources
     - Search for stale ``res://`` paths after moving files under ``assets/``.
   * - Sensor payload schema changed
     - Update Godot sensor output and Python schema validation utilities together.
   * - Exported datasets are too large
     - Use ignored export folders and avoid committing generated data to GitHub.

Diagnostic check
----------------

.. code-block:: python

   from oceansim_client import OceanSimClient

   client = OceanSimClient(timeout=3.0)
   assert client.connect(retry=False)
   print(client.send_command("get_state"))
   print(client.send_command("get_sensors"))
   client.disconnect()
