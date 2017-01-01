import BinLib
import IS


class PROM:
    def __init__(self):
        self.TickTime = 0
        self.currentTick = 0
    def tick(self,ram,prom):
        control = ram.read(0)
        addr = int(BinLib.toTwoComp(ram.read(1)),2)
        if control == 1: #read 
            ram.write(2,prom.read(addr).AsNumber)
        elif control == 2:
            t = BinLib.toTwoComp(ram.read(2))
            prom.write(addr,IS.Instruction(t[0:4],t[4:8],t[8:12],t[12:16]))
            
    def CleanUp(self):
        pass
        