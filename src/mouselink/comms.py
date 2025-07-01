import json
import pack
class sl_messages: 
    device_list_message = '{"jsonrpc":"2.0","method":"didReceiveMessage","params":{"encoding":"base64","message":"JAAAAAIefn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fgE="}}'
    def connection_start(self, message):
        data = {
            "jsonrpc": "2.0", "id": None, "result": None
        }
        data["id"] = self.getId(message)
        return json.dumps(data)
    def connection_info(self, ping):
        data = {
            "jsonrpc":"2.0","method":"didDiscoverPeripheral","params":{"peripheralId":"virtual_ev3","name":"Emulated EV3","rssi":-1000}
        }
        data["rssi"] = ping
        return json.dumps(data)
    def getMethod(self, message):
        data = json.loads(message)
        method = data["method"]
        return method
    def getId(self, message):
        data = json.loads(message)
        id = data["id"]
        return id
class ev3protocol:
    def __init__(self):
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
        if data not in self.types.keys():
            return False
        else:
            return True
    def read(self,data,func):
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
        jsondata = {
            "jsonrpc":"2.0","method":"didReceiveMessage","params":{"encoding":"base64","message":""}
        }
        jsondata["params"]["message"] = data
        return json.dumps(jsondata)
    def _tosend(self,devicereq):
        if devicereq:
            return sl_messages.device_list_message
        else:
            return self.jsonify(self._buildmessage())
    def _buildmessage(self):
        if self.writeBuffer == []:
            res=pack.pack_dist(0)
        else:
            
            res=pack.pack_dist(self.writeBuffer[0]) 
            try:
                self.writeBuffer = self.writeBuffer[1:] 
            except:
                self.writeBuffer = []
            
        return res 