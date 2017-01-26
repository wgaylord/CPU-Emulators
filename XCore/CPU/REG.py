class REG:
    def __init__(self,size=1):
        self.data = {}
        self.size = size

    def read(self,address):
        try:
            #print self.data[address]
            return self.data[address]
        except KeyError:
            return 0

    def write(self,address,data):

        if address > self.size -1:
            raise Exception("Addressing outside of REG")
        if data == 0:
            try:
                del self.data[address]
            except:
                pass
        else:
            self.data[address] = data

