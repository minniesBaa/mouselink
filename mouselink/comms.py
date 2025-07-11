"""
File for handling communications and some message construction
"""

import json
from . import pack
class sl_messages_ev3: 
    # class with all the JSON message construction functions
    @staticmethod
    def device_list():
        # returns a message for responding to Scratch's requests for the devices plugged into the peripheral
        data = {
            "jsonrpc":"2.0","method":"didReceiveMessage","params":{"encoding":"base64","message":"JAAAAAIefn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fgE="}
            } # this is captured from a real EV3, with one dist sensor on sensor 1.
        return json.dumps(data)
    def connection_start(self, message):
        # construct a message to initiate a connection with Scratch
        data = {
            "jsonrpc": "2.0", "id": None, "result": None
        }
        data["id"] = self.getId(message)
        return json.dumps(data)
    def connection_info(self, ping, name):
        # send Scratch a message saying that a fake EV3 peripheral *totally* exists
        data = {
            "jsonrpc":"2.0","method":"didDiscoverPeripheral","params":{"peripheralId":"mouselink_device","name":None,"rssi":-1000}
        }
        data["rssi"] = ping
        data["params"]["name"] = name
        return json.dumps(data)
    def getMethod(self, message):
         # get the message method from a jsonrpc message
        data = json.loads(message)
        method = data["method"]
        return method
    def getPayload(self, message):
         # get the payload from jsonrpc message
        data = json.loads(message)
        payload = data["params"]["message"]
        return payload
    def getId(self, message):
        # gets the message ID from a jsonrpc message
        data = json.loads(message)
        id = data["id"]
        return id
class ev3protocol:
    # a (janky) protocol for communicating with Scratch
    def __init__(self):
        # init function - set some variables
        self.readBuffer = ""
        self.writeBuffer = []
        self.isReading = False
        self.writetypes = [
            100,
            1,
            2,
            3,
            4
        ]
        self.types = {
            "DwAAAIAAAJQBgQKC9gCCAQA=": 0, # new message, note 0 
            "DwAAAIAAAJQBgQKCJQGCAQA=": 1, # end message, note 50
            "DwAAAIAAAJQBgQKCLQiCAQA=": 2, # a 0, note 84
            "DwAAAIAAAJQBgQKCchOCAQA=": 3  # a 1, note 130
        }
    def val(self,data):
        # validate if the data is acceptable by the protocol
        if data not in self.types.keys():
            return False
        else:
            return True
    def read(self,data,func):
        # read one bit from the project
        char = self.types[data]
        match char:
            case 0:
                self.isReading = True
                self.readBuffer = ""
            case 1:
                self.isReading = False
                func(self.readBuffer)
            case 2:
                self.readBuffer = f"{self.readBuffer}0"
            case 3:
                self.readBuffer = f"{self.readBuffer}1"
    def write(self,data):
        # write some data to the project
        buffer = [self.writetypes[1],self.writetypes[0]]
        for bit in data:
            match bit:
                case "0":
                    buffer.append(self.writetypes[3])
                    buffer.append(self.writetypes[0])
                case "1":
                    buffer.append(self.writetypes[4])
                    buffer.append(self.writetypes[0])
                case _:
                    continue
        buffer.append(self.writetypes[2])
        self.writeBuffer = buffer
    def jsonify(self,data):
        # create a json message with special data in the params/message field
        jsondata = {
            "jsonrpc":"2.0","method":"didReceiveMessage","params":{"encoding":"base64","message":""}
        }
        jsondata["params"]["message"] = data
        return json.dumps(jsondata)
    def _tosend(self,devicereq):
        # decides what data to send to the project
        if devicereq:
            return sl_messages_ev3.device_list()
        else:
            return self.jsonify(self._buildmessage())
    def _buildmessage(self):
        # constructs a message to a list that is sent bit by bit
        if self.writeBuffer == []:
            res=pack.pack_dist(0)
        else:
            
            res=pack.pack_dist(self.writeBuffer[0]) 
            try:
                self.writeBuffer = self.writeBuffer[1:] 
            except:
                self.writeBuffer = []
            
        return res 
    
class sl_messages_microbit(sl_messages_ev3):
    @staticmethod
    def on_read_req():
        data = {
            "jsonrpc":"2.0","id":2,"result":    {
                    "encoding":"base64","message":"AAAAOQAAAAAAAAAAAAAAAAAAAAA="
                }
            }
        return json.dumps(data)
    @staticmethod
    def got_message():
        data = {
            "jsonrpc":"2.0","id":0,"result":    {
                    "encoding":"base64","message":"AAAAOQAAAAAAAAAAAAAAAAAAAAA="
                }
            }
        return json.dumps(data)
    @staticmethod
    def make_microbit_packet(b64):
        data = {
            "jsonrpc":"2.0","method":"characteristicDidChange","params":    {
                        "serviceId":"0000f005-0000-1000-8000-00805f9b34fb","characteristicId":"5261da01-fa7e-42ab-850b-7c80220097cc","encoding":"base64","message":None
                    }
                }
        data["params"]["message"] = b64
        return json.dumps(data)
class microbitprotocol:
    def __init__(self):
        pass
    def write(self):
        pass
    def read(self, message, onread):
        if onread is not None:
            onread(pack.microbit_load_matrix(json.loads(message)["params"]["message"]))
        else:
            print("Set your on_read function to respond to messages from Scratch!")
    def val(self):
        pass