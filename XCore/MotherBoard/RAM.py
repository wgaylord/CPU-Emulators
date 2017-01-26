import json

from MotherBoard import util


class RAM():
    def __init__(self,size=1):
        self.data = {}
        self.size = size

    def read(self,address):
        try:
            return self.data[address]
        except KeyError:
            return 0

    def write(self,address,data):
        if address > self.size -1:
            raise Exception("Addressing outside of RAM")
        if data == 0:
            del self.data[address]
        else:
            self.data[address] = data

    def dumps(self):
        out = ""
        for x in xrange(self.size):
            out = out + str(x)+ " : " + util.mybin(self.read(x)) + ","
        return out

    def dump(self,file):
        t = self.data.copy()
        t["size"] = self.size
        json.dump(t,file)

    def loads(self,s):
        try:
            size = 0
            for x in s.split(","):
                t = x.split(" : ")
                size = int(t[0])
                self.write(int(t[0]), util.myint(t[1]))
            self.size = size+1
        except IndexError:
            raise Exception("Attempted to load invalid RAM dump")

    def load(self,file):
        try:
            t = json.load(file)
            self.size = t["size"]
            del t["size"]
            self.data = t
        except KeyError:
            raise Exception("Attempted to load invalid RAM dump")
