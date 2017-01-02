import urllib
import BinLib
from PIL import Image
from threading import Thread

RAM = [16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]

"""
RAM for screen
Memory mapped each cell is one row of pixels
""" 
buffer = Image.new("L",(16,16))   
def screen():
    global buffer
    while True:
       for x in xrange(16):
            #print RAM[x],ram.read(RAM[x])
            line = ""
            for y in xrange(16):
                if buffer.getpixel((y,x)) == 255:
                    line = line + "1"
                else:
                    line = line + "0"
            try:
                urllib.urlopen("http://192.168.1.74:8000/?line="+line+"&row="+str(x))
            except:
                pass

class MemMappedRemoteScreen:
    def __init__(self):
        self.url = "192.168.1.74:8000"
        self.TickTime = 0
        self.currentTick = 0
        self.screenThread = Thread(target=screen)
        self.screenThread.start()
    def tick(self,ram,prom):
        
        for x in xrange(0,16):
            #print RAM[x],ram.read(RAM[x])
            q = BinLib.toTwoComp(ram.read(RAM[x]))
            for y in xrange(16):
                buffer.putpixel((y,x),255*int(q[y]))
        
    def CleanUp(self):
        pass