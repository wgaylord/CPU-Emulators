import MotherBoard.util as util

class PROM:
    def __init__(self,size=1):
        self.data = {}
        self.size = size
    
    def read(self,address):
        if address > self.size -1:
            raise Exception("Addressing outside of PROM")
        try:
            return self.data[address]
        except KeyError:
            return 0

    def write(self,address,data):
        if address > self.size -1:
            raise Exception("Addressing outside of PROM")
        if data == 0:
            try:
                del self.data[address]
            except:
                pass
        else:
            self.data[address] = data

    def loadPromFromBin(self, file):
        def toInt(first, second):
            first = ord(first)
            second = ord(second)
            return ((first << 8) | (second))

        addr = 0
        f = open(file, "rb")
        number = 0
        while True:
            try:
                ord(f.read(1))
                number += .5
            except:
                break
        f.seek(0)
        # print number
        for x in xrange(int(number)):
            num = toInt(f.read(1), f.read(1))
            self.write(addr, num)
            addr += 1

        f.close()

