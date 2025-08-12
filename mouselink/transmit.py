class feed:
    def __init__(self, peripheralInstance):
        self.p = peripheralInstance
        self.t = self.p.type
        self.started = False
        self.encoding = {
            
        }
    def send(self, name, data):
        ...