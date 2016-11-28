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
                
    def exportRegs(self):
        return self.__regs
    
    def importRegs(self,reg):
        self.__regs = reg

class ram:
    def __init__(self,size,fill = 0):
        self.__ram = [fill]*size 
        
    
    def write(self,addr,data):
       
        self.__ram[addr] = data
    
    def read(self,addr):
        
        return self.__ram[addr]
        
    def exportRAM(self):
        return self.__ram
     
    def importRAM(self,ram):
        self.__ram = ram
        
        
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
    RAM = ram(16)#(2**15))
    PROM = ram((2**16),IS.Instruction('0000','0000','0000','0000'))
    
    def __init__(self):
        pass
            
    def loadProm(self,file):
        addr = 0
        f = open(file)
        t = f.readlines()
        for x in t:
            y = x.split(' ')
            if y[0] in IS.str2OP.keys():
                self.PROM.write(addr,IS.Instruction(bin(IS.str2OP[y[0]])[2:],y[1],y[2],y[3]))
            else:
                self.PROM.write(addr,IS.Instruction(y[0],y[1],y[2],y[3]))
            addr +=1
        