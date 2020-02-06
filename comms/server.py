"""Transport module for receiving data from Workers"""

import json

class Server():
      def __init__(self):
            """Whatever is needed for socket stuff"""
            pass

      def __fake_receive_from_client(self):
            """This is all happening on the client.  __ means private."""
            # Make the call
            dat_dict = {"type": "init"}
            # type(dat_dict) == <class 'dict'>
            dat_json = json.dumps(dat_dict)
            # type(dat_json) == <class 'str'>
            dat_raw = dat_json.encode()
            # type(dat_raw) == <class 'bytes'>
            return(dat_raw)

      def run(self, make_response):
            """This is what master calls."""
            # Do the socket stuff to receive "data" from client
            dat = self.__fake_receive_from_client().decode()

            resp = make_response(dat)    # Call the function you've been given

            # Do the socket stuff to send "resp" to the client

            # And probably repeat forever!
