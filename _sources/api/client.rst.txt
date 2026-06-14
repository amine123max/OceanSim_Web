OceanSim Client
===============

The :mod:`oceansim_client.client` module provides the low-level TCP transport used by higher-level APIs. It manages sockets, request IDs, background receiving, pending responses, timeout handling, and protocol errors.

Classes
-------

.. py:class:: OceanSimClient(host="localhost", port=9876, timeout=5.0)

   TCP client for OceanSim's protocol.

   :param str host: simulator hostname.
   :param int port: simulator TCP port.
   :param float timeout: default response timeout in seconds.

   .. py:attribute:: PROTOCOL_VERSION

      Current protocol version. The value is ``2``.

   .. py:attribute:: is_connected

      ``True`` when the TCP socket is connected.

   .. py:method:: launch_godot(exe_path=None)

      Start a packaged simulator executable before connecting.

   .. py:method:: connect(retry=True, max_retries=10, retry_interval=1.0)

      Open the TCP socket and start the background receive loop.

      :returns: ``True`` on success, ``False`` on connection failure.

   .. py:method:: disconnect()

      Close the socket and terminate a launched Godot process if present.

   .. py:method:: send(msg)

      Send a raw JSON message with a trailing newline.

      :param dict msg: protocol request object.
      :returns: ``True`` if the message was sent.

   .. py:method:: send_command(action, data=None, timeout=None)

      Build a ``command`` request, inject ``protocol_version`` and ``request_id``, send it, and wait for a matching state, response, or error envelope.

      :raises OceanSimConnectionError: when the simulator is disconnected.
      :raises OceanSimTimeoutError: when no response arrives before timeout.
      :raises OceanSimProtocolError: when the simulator returns an error envelope.

   .. py:method:: send_sim_control(action, timeout=None, **kwargs)

      Send a ``sim_control`` request such as ``reset``, ``pause``, ``resume``, or ``set_time_scale``.

   .. py:method:: send_batch(requests, timeout=None)

      Normalize each child request with protocol version and request ID, then send a top-level batch request.

      :param list requests: command or sim-control dictionaries.
      :returns: response envelope whose data contains ``count`` and ``responses``.

   .. py:method:: request_state()

      Convenience wrapper for ``send_command("get_state")``. Returns the response data dictionary.

   .. py:method:: get_latest_state()

      Return the latest cached state without sending a new request.

Exceptions
----------

.. py:exception:: OceanSimError

   Base SDK failure.

.. py:exception:: OceanSimConnectionError

   Raised when a command cannot be sent because the simulator is absent or disconnected.

.. py:exception:: OceanSimTimeoutError

   Raised when the simulator does not answer before the selected timeout.

.. py:exception:: OceanSimProtocolError

   Raised when the simulator returns an error envelope, empty response, or mismatched request ID.

Example
-------

.. code-block:: python

   from oceansim_client import OceanSimClient

   with OceanSimClient(timeout=5.0) as client:
       state = client.request_state()
       batch = client.send_batch([
           {"type": "command", "action": "get_sensors"},
           {"type": "command", "action": "set_force", "data": {"force": [0, 80, 0]}},
       ])
