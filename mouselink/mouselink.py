from websockets.sync.server import serve as _serve # websocket server
from . import comms
import threading
import time
import json

devices = "CwAAAAAhAJiBIGDhIA==" # the base64 sent by Scratch when requesting the devices connected to a peripheral

onread = None # variable to store users' on_read function
onconn = None # variable to store users' on_connect function

def _run(e): # call the on_load function
    if e is not None:
        try:
            onread(e)
        except:
            raise ValueError("on_read is incorrectly set!")
        
def _onconn(e): # call the on_load function
    if e is not None:
        try:
            onconn(e)
        except:
            raise ValueError("on_connect is incorrectly set!")

class _peripheral: # class that every peripheral inherits from
    def __init__(self): #### TEMP - just so i can verify methods exist via vscode
        self._sl = comms.sl_messages_ev3()
        self._comm = comms.ev3protocol()
    def send(self,data):
        # send data to Scratch via the peripheral class's _comm object
        self._comm.write(data)
    def run(self):
        # starts the websocket server for use by Scratch
        try:
            self._main()
        except:
            raise OSError("Error starting the websocket server! Make sure you have stopped Scratch Link.")
    def _main(self): # function to serve the server
        with _serve(self._link, "localhost", 20111) as server:
            server_thread = threading.Thread(target=server.serve_forever, daemon=True)
            server_thread.start()
            try:
                while server_thread.is_alive():
                    time.sleep(0.5)
            except:
                server.shutdown()
    def on_read(self,func): # set the onread function
        global onread
        onread = func
    def on_connect(self,func): # set the onconn function
        global onconn
        onconn = func
class ev3(_peripheral):
    # an ev3 peripheral class
    def __init__(self):
        self._sl = comms.sl_messages_ev3() # set comms and sl objects
        self._comm = comms.ev3protocol()
        self.name = "Mouselink Device"
    def _link(self,websocket):
        # websocket connection handler for EV3
        global devices
        for message in websocket:
            devicereq = False
            if self._sl.getMethod(message) == "discover": # check if Scratch is looking for devices
                websocket.send(self._sl.connection_start(message))
                websocket.send(self._sl.connection_info(-500, self.name))
            if self._sl.getMethod(message) == "connect": # when scratch picks a peripheral
                _onconn()
                websocket.send(self._sl.connection_start(message))
            if self._sl.getMethod(message) == "send": # when connection is live and data is being sent
                data = self._sl.getPayload(message)
                if devices == data:
                    devicereq = True
                websocket.send(self._comm._tosend(devicereq))
                if self._comm.val(data):
                    self._comm.read(data, _run)

class microbit(_peripheral):
    def __init__(self):
        self._sl = comms.sl_messages_microbit() # set comms and sl objects
        # self._comm = comms.ev3protocol() # removed until one is developed for micro:bit
        self.name = "Mouselink Device"
    def _link(self,sock):
        while True:
            try:
                message = sock.recv(timeout=0.1)
                match self._sl.getMethod(message):
                    case "discover":
                        sock.send(self._sl.connection_info(-500, self.name))
                    case "connect":
                        sock.send(self._sl.connection_start(message))
                    case "write":
                        sock.send(self._sl.got_message())
                        data = {"jsonrpc":"2.0","id":4,"result":0}
                        data["id"] = self._sl.getId(message)
                        sock.send(json.dumps(data))
                    case "read": 
                        sock.send(self._sl.on_read_req())
                    case _:
                        pass
            except TimeoutError:
                sock.send(self._sl.make_microbit_packet("/2kAOQAAAAAAAAAAAAAAAAAAAAA="))
            except Exception as e:
                break
            time.sleep(0.1)