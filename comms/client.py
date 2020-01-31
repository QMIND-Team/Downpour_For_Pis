"""Transport module for sending strings to the manager."""

import json

class Client():
      def __init__(self):
            """Whatever is needed for socket stuff"""
            pass

      def __fake_send_to_server(self, data):
            """This is all happening on the server.  __ means private."""
            # Make the response
            resp_dict = {"type": "init_resp", "id": 7}
            # type(resp_dict) == <class 'dict'>
            resp_json = json.dumps(resp_dict)
            # type(resp_json) == <class 'str'>
            resp_raw = resp_json.encode()
            # type(resp_raw) == <class 'bytes'>
            return(resp_raw)

      def send(self, data: str):
            """This is what worker calls."""
            # Do the socket stuff to send "data" to the server
            # Do the socket stuff to get "resp" from the server
            resp_raw = self.__fake_send_to_server(data)
            # type(resp_raw) == <class 'bytes'>
            resp = resp_raw.decode()
            # type(resp) == <class 'str'>

            return resp
