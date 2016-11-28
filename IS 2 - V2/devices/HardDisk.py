
RAM_ADDRESSES = [2,3,4] #addr,control,data
INTURRPT = 16 #called when read finished

def binSplit(x):
    t = ""
    if x*-1 > x:
        t = bin(x)[3:]
    else:
        t = bin(x)[2:]
    t = ("{0:0>%s}" % (16)).format(t)
    if bin(x)[0] == "-":
        return bytearray([1,int(t[:10],2),int(t[10:],2)])
    else:
        return bytearray([0,int(t[:10],2),int(t[10:],2)])
   
def binJoin(sign,x,y):
    return int(("-"*sign) + bin(x) + bin(y)[2:],2)

class HardDisk:
    
    data = open("test.bin","r+b")
    
    
    def tick(self,ram,prom):
        addr = int(bin(ram.read(3))[2:4]+bin(ram.read(2))[2:],2)
        control = int(bin(ram.read(3))[2:][4:],2)
        data.seek(3*addr)
        if control == 0: #Read disk
            
            bytes = data.read(3)
            ram.write(4,binJoin(bytes[0],bytes[1],bytes[2]))
            return 16
        elif control = 1: #write disk
            data.write(binSplit(ram.read(4)))
            data.flush()

    def CleanUp(self):
        data.close()