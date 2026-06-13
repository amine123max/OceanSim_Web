Installation
============

OceanSim is split into a Godot simulator project and an editable Python SDK package. The simulator owns the real-time runtime and exposes TCP port ``9876`` by default. The Python SDK connects to that running process for external control, sensing, recording, and replay.

Requirements
------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Requirement
     - Purpose
   * - Godot 4.5+
     - Open and run ``project.godot`` in the ``oceansim`` folder.
   * - Python 3.8+
     - Install and run ``oceansim_client``.
   * - NumPy
     - Required by the SDK for state vectors, point clouds, mapping, and coordinate conversion.
   * - Gymnasium optional
     - Required only for Gym-style reinforcement-learning examples.

Run the simulator
-----------------

Open the Godot project and run the configured entry scene, ``res://scenes/FrontView.tscn``.

.. code-block:: powershell

   cd C:\path\to\OceanSim\oceansim
   godot --path .

Install the SDK
---------------

Install the Python package from the project-local ``python`` folder. Editable mode is recommended while the simulator and SDK are evolving together.

.. code-block:: powershell

   cd C:\path\to\OceanSim\oceansim
   pip install -e python
   pip install -e "python[all]"   # optional Gym examples

Connection check
----------------

.. code-block:: python

   from oceansim_client import OceanSimClient

   client = OceanSimClient(host="localhost", port=9876, timeout=5.0)
   if client.connect():
       response = client.send_command("get_state")
       print(response["type"], response.get("status"))
       client.disconnect()

If the client cannot connect, confirm that the Godot project is running and that no other process is using port ``9876``.
