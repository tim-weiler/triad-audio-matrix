import socket
import logging

from .matrix_commands import (
    setOutputToInput,
    setOutputVolume
)

_LOGGER = logging.getLogger(__name__)

def send_tcp_command(command, host, port):
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.settimeout(300)
    sock.setblocking(1)

    try:
        #_LOGGER.warn("Sending " + command.hex())
        sock.sendall(command)
        data = sock.recv(1024)
        received = str(data)
        #_LOGGER.warn("Received: " + str(received))

    except socket.timeout:
        received = "Timeout occurred during data reception"
        _LOGGER.warn(received)
    except Exception as e:
        received = {e}
        _LOGGER.warn("Exception " + str(received))
    finally:
        sock.close()


    return received


class TriadMatrixOutputChannel(object):
# Represents an output channel of an Triad Audio Matrix

    def __init__(self, host, port, channel):
        self._host = host
        self._port = port
        self._channel = channel
        self._source = 0
        self._volume = 0

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def channel(self):
        return self._channel

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self,value):
        self._source = value
        data = setOutputToInput[:]
        data.append(self._channel-1)
        
        if self._source == 0:
            # this disconnects the output
            # send an 8 for an 8 channel matrix
            data.append(16)
        else:
            data.append(self._source-1)

        send_tcp_command(data, self._host, self._port)
        return 1

    @source.deleter
    def source(self):
        del self._source

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self,value):
        self._volume = value
        data = setOutputVolume[:]
        data.append(self._channel-1)

        new_volume = int(float(self._volume) * 160)
        data.append(new_volume)
        send_tcp_command(data, self._host, self._port)
        return 1

    @volume.deleter
    def volume(self):
        del self._volume