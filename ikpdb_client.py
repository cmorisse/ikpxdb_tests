# coding: utf-8

import socket
import logging
import json
import ikpdb

_logger = logging.getLogger(__file__)
_logger.addHandler(logging.StreamHandler())
_logger.setLevel(logging.INFO)



class IKPdbConnectionError(Exception):
    pass

class IKPdbClientError(Exception):
    pass

class IKPdbClient(object):
    
    MAGIC_CODE = "LLADpcdtbdpac"
    MESSAGE_TEMPLATE = "length=%%s%s%%s" % MAGIC_CODE
    SOCKET_BUFFER_SIZE = 4096  # Maximum size of a packet received from client
    
    def __init__(self, host, port=15470, debug=False):
        """ Create a client and connect to IKPdbClient
        """
        self._host = host
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._host, self._port))
        self._received_data = ''
        self._msg_id = 100
    
        if not debug:
            obj = self.receive()
            assert obj['info_messages'][0] == u"Welcome to", "'start'/'Welcome to...' message not received"
    
    def encode(self, obj):
        json_obj = json.dumps(obj)
        return self.MESSAGE_TEMPLATE % (len(json_obj), json_obj,)
    
    def decode(self, message):
        json_obj = message.split(self.MAGIC_CODE)[1]
        obj = json.loads(json_obj)
        return obj

    def log_received(self, msg):
        _logger.debug("Received %s bytes >>>%s<<<", len(msg), msg)

    def log_sent(self, msg):
        _logger.debug("Sent %s bytes >>>%s<<<", len(msg), msg)        
        
    def receive(self, timeout=None):
        """
        """
        if timeout:
            self._socket.settimeout(timeout)
        else:
            self._socket.settimeout(None)

        skip_recv_switch = True if self._received_data else False
        
        while True:
            try:
                if skip_recv_switch:
                    data = ''
                    skip_recv_switch = False 
                else:
                    data = self._socket.recv(self.SOCKET_BUFFER_SIZE)
            except socket.error as socket_err:
                return {'command': '_InternalQuit', 
                        'args':{'socket_error_number': socket_err.errno,
                                'socket_error_str': socket_err.strerror}}
            self._received_data += data
                
            # Do we have received a MAGIC_CODE
            try:
                magic_code_idx = self._received_data.index(self.MAGIC_CODE)
            except ValueError:
                continue
            
            # Do we have we received a length=
            try:
                length_idx = self._received_data.index('length=')
            except ValueError:
                continue
            
            # extract length content from received data
            json_length = int(self._received_data[length_idx + 7:magic_code_idx])
            message_length = magic_code_idx + len(self.MAGIC_CODE) + json_length
            if len(self._received_data) >= message_length:
                full_message = self._received_data[:message_length]
                self._received_data = self._received_data[message_length:]
                break
            else:
                self.SOCKET_BUFFER_SIZE = message_length - len(self._received_data)

        self.log_received(full_message)
        obj = self.decode(full_message)
        return obj

    def send(self, command, **kwargs):
        """ Build a message from parameters and send it to debugger.
        
        :param command: The command sent to the debugger
        :type command: str
        
        :param _id: Unique id of the sent message. It is generated by the client. 
                    but it can be forced.Right now, it's always `None`
                    for messages from debugger to client.
        :type _id: int
        """
        msg = self.encode({
            '_id': self._msg_id,
            'command': command,
            'args': kwargs
        })
        self._msg_id += 1
        if self._socket:
            send_bytes_count = self._socket.sendall(msg)
            self.log_sent(msg)
            return self._msg_id - 1
        raise IKPdbConnectionError("Connection lost!")

    ##### here are high level method #####
    def run_script(self):
        msg_id = self.send('runScript')
        reply_msg = self.receive()
        assert reply_msg['_id'] == msg_id, "Unexpected reply message to runScript command."
        assert reply_msg['commandExecStatus'] == "ok", "IKPdb failed to start debugged program."
        return reply_msg

    def resume(self):
        msg_id = self.send('resume')
        reply_msg = self.receive()
        print(reply_msg['_id'], msg_id)
        assert reply_msg['_id'] == msg_id, "Unexpected reply message to resume command."
        assert reply_msg['commandExecStatus'] == "ok", "IKPdb failed to resume debugged program."
        assert reply_msg['result'].get('executionStatus') == 'running', "IKPdb failed to resume debugged program."
        return reply_msg

    def suspend(self):
        msg_id = self.send('suspend')
        reply_msg = self.receive()
        print(reply_msg['_id'], msg_id)
        assert reply_msg['_id'] == msg_id, "Unexpected reply message to 'suspend' command."
        assert reply_msg['commandExecStatus'] == "ok", "IKPdb failed to resume debugged program."
        assert reply_msg['result'].get('executionStatus') == 'running', "IKPdb failed to resume debugged program."
        return reply_msg

    def set_breakpoint(self, file_name, line_number, enabled=True, condition=None):
        msg_id = self.send('setBreakpoint',
                           file_name=file_name,
                           line_number=line_number,
                           enabled=enabled,
                           condition=condition)
        reply_msg = self.receive()
        assert reply_msg['_id'] == msg_id, "Unexpected reply to setBreakpoint."
        assert reply_msg['commandExecStatus'] == 'ok', "Failed to setBreakpoint."
        return reply_msg

    def get_breakpoints(self):
        msg_id = self.send('getBreakpoints')
        reply_msg = self.receive()
        assert reply_msg['_id']==msg_id, "Unexpected reply to getBreakpoints."
        assert reply_msg['commandExecStatus']=="ok", "getBreakpoints failed."
        return reply_msg['result']

    def change_breakpoint_state(self, breakpoint_number, enabled, condition):
        msg_id = self.send('changeBreakpointState',
                           breakpoint_number=breakpoint_number,
                           enabled=enabled,
                           condition=condition)
        reply_msg = self.receive()
        if reply_msg['_id'] != msg_id:
            raise IKPdbClientError("Unexpected reply message to 'changeBreakpointState'.")
        if reply_msg['commandExecStatus'] != "ok":
            raise IKPdbClientError("'changeBreakpointState' command failed.")
        return reply_msg

    def clear_breakpoint(self, breakpoint_number):
        msg_id = self.send('clearBreakpoint',
                           breakpoint_number=breakpoint_number)
        reply_msg = self.receive()
        if reply_msg['_id'] != msg_id:
            raise IKPdbClientError("Unexpected reply message to 'changeBreakpointState'.")
        if reply_msg['commandExecStatus'] != "ok":
            raise IKPdbClientError("'clearBreakpoint' command failed.")
        return reply_msg
