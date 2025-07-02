from websockets.sync.server import serve as _serve # websocket server
from . import comms
import threading
import time

devices = "CwAAAAAhAJiBIGDhIA==" # the base64 sent by Scratch when requesting the devices connected to a peripheral

onread = None # variable to store users' on_load function

def _run(e): # call the on_load function
    onread(e)

class _peripheral: # class that every peripheral inherits from
    def __init__(self): #### TEMP - just so i can verify methods exist via vscode
        self._sl = comms.sl_messages_ev3()
        self._comm = comms.ev3protocol()
    def send(self,data):
        # send data to Scratch via the peripheral class's _comm object
        self._comm.write(data)
    def run(self):
        # starts the websocket server for use by Scratch
        self._main()
    def _link(self,websocket):
        # websocket connection handler
        global devices
        for message in websocket:
            devicereq = False
            if self._sl.getMethod(message) == "discover": # check if Scratch is looking for devices
                websocket.send(self._sl.connection_start(message))
                websocket.send(self._sl.connection_info(-500))
            if self._sl.getMethod(message) == "connect": # when scratch picks a peripheral
                websocket.send(self._sl.connection_start(message))
            if self._sl.getMethod(message) == "send": # when connection is live and data is being sent
                data = self._sl.getPayload(message)
                if devices == data:
                    devicereq = True
                websocket.send(self._comm._tosend(devicereq))
                if self._comm.val(data):
                    self._comm.read(data, _run)
    def _main(self): # function to serve the server
        with _serve(self._link, "localhost", 20111) as server:
            server_thread = threading.Thread(target=server.serve_forever, daemon=True)
            server_thread.start()
            try:
                while server_thread.is_alive():
                    time.sleep(0.5)
            except:
                server.shutdown()
    def _onread(self): # run the onread function
        if self.onread is not None:
            self.onread
    def on_read(self,func): # set the onread function
        global onread
        onread = func
class ev3(_peripheral):
    # an ev3 peripheral class
    def __init__(self):
        self._sl = comms.sl_messages_ev3() # set comms and sl objects
        self._comm = comms.ev3protocol()
