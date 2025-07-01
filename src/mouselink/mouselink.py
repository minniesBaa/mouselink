from websockets.sync.server import serve as _serve
import comms
import json

devices = "CwAAAAAhAJiBIGDhIA=="

onread = None

def _run(e):
    onread(e)

class _peripheral:
    def send(self,data):
        self._comm.write(data)
    def run(self):
        self._main()
    def _link(self,websocket):
        global devices
        for message in websocket:
            devicereq = False
            if self._sl.getMethod(message) == "discover":
                websocket.send(self._sl.connection_start(message))
                websocket.send(self._sl.connection_info(-500))
            if self._sl.getMethod(message) == "connect":
                websocket.send(self._sl.connection_start(message))
            if self._sl.getMethod(message) == "send":
                #id = json.loads(message)["id"]
                data = json.loads(message)["params"]["message"]
                if devices == data:
                    devicereq = True
                websocket.send(self._comm._tosend(devicereq))
                if self._comm.val(data):
                    self._comm.read(data, _run)
    def _main(self):
        with _serve(self._link, "localhost", 20111) as server:
            server.serve_forever()
    def _onread(self):
        if self.onread is not None:
            self.onread
    def on_read(self,func):
        global onread
        onread = func
class ev3(_peripheral):
    def __init__(self):
        self._sl = comms.sl_messages()
        self._comm = comms.ev3protocol()
