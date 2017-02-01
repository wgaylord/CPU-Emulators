import BinLib
import IS

class regs:
    __regs = []
    
    def __init__(self,regNum):
        for x in xrange(regNum):
            self.__regs.append(0)
            
    def read(self,num):
        
        try:    
            return self.__regs[num]
        except:
            raise Exception
            
    def write(self,num,data,clampZero= True):
        
        if num == 0 and clampZero:
            return 
        else:
            try:
                #print num,data
                self.__regs[num] = data
            except:
                raise Exception
                
    def exportREG(self):
        return self.__regs
    
    def importREG(self,reg):
        self.__regs = reg

class ram:
    def __init__(self,size,fill = 0):
        self.data = [fill]*size 
        
    
    def write(self,addr,data):
        try:
            self.data[addr] = data
        except:
            print addr
    def read(self,addr):
        
        return self.data[addr]
        
    def exportRAM(self):
        return self.data
     
    def importRAM(self,ram):
        self.data = ram
        
        
class stack:
    
    __stack = []
    
    def __init__(self,size):
        self.__maxDepth = size
        self.__currentDepth = 0
        
    def push(self,data):
        if self.__currentDepth < self.__maxDepth:
            self.__stack.append(data)
            self.__currentDepth += 1
        else:
            raise Exception
    
    def pop(self):
        if self.__currentDepth >= 1: 
            self.__currentDepth -=1
            return self.__stack.pop()
        else:
            raise Exception
            
    def exportStack(self):
        return self.__stack
        
    def importStack(self,stak):
        self.__stack = stak
        
class memory:
    Stack = stack(256)
    REG = regs(16)
    RAM = ram((2**15))
    PROM = ram((2**16),IS.Instruction('0000','0000','0000','0000'))
    
    def __init__(self):
        pass
            
    def loadPromSudoASM(self,file):
        addr = 0
        f = open(file)
        t = f.readlines()
        for x in t:
            y = x.split(' ')
            if y[0].upper() in IS.str2OP.keys():
                self.PROM.write(addr,IS.Instruction(bin(IS.str2OP[y[0]])[2:],y[1],y[2],y[3]))
            else:
                self.PROM.write(addr,IS.Instruction(y[0],y[1],y[2],y[3]))
            addr +=1
            
    def loadPromFromBin(self,file):
        def toInt(first,second):
            first=ord(first)
            second=ord(second)
            return ((first<<8)|(second))
            
        addr = 0
        f = open(file,"rb")
        number = 0
        while True:
            try:
                ord(f.read(1))
                number +=.5
            except:
                break
        f.seek(0)
        #print number
        for x in xrange(int(number)):
            num = toInt(f.read(1),f.read(1))
            #print num
            b = bin(num)[2:]
            b= ("{0:0>%s}" % (16)).format(b)
            #print b,len(b)
            self.PROM.write(addr,IS.Instruction(b[0:4],b[4:8],b[8:12],b[12:16]))
            addr +=1
        
        f.close()
        #exit()
        