import IS
import BinLib

class cpu:
    inIntruppt = False
    intrupptTable = [None]*256
    intrupptCalled = [False]*256
    intrupptTimer = [-1]*256
    currentInstruction = IS.Instruction('0000','0000','0000','0000')
    return_addr = 0
    current_int = -1
    
    def __init__(self,Memory):
        self.PC = 0
        self.memory = Memory
        
    
    def fetchIS(self):
        inst = self.memory.PROM.read(self.PC)
        
        if inst.isMutliPart():
            inst.second = self.memory.PROM.read(self.PC+1)
            self.PC = self.PC + 1
        self.currentInstruction = inst
    def scheduleIntrrupt(self,intruppt):
        self.intrupptCalled[intruppt] = True
        
    def execute(self):
        #print self.currentInstruction.raw
        if self.currentInstruction.op_int == IS.ADD:
            
            q = self.memory.REG.read(self.currentInstruction.A_int)+self.memory.REG.read(self.currentInstruction.B_int)
            w = BinLib.fromTwoComp(BinLib.toTwoComp(q))
            if not q == w:
                self.scheduleIntrrupt(4) #Overflow
            self.memory.REG.write(self.currentInstruction.C_int,w)
        elif self.currentInstruction.op_int == IS.ADDi:
            q = self.memory.REG.read(self.currentInstruction.A_int)+self.memory.REG.read(self.currentInstruction.B_int)+1
            w = BinLib.fromTwoComp(BinLib.toTwoComp(q))
            if not q == w:
                self.scheduleIntrrupt(4) #Overflow
            self.memory.REG.write(self.currentInstruction.C_int,w)
        elif self.currentInstruction.op_int == IS.SUB:
            q = self.memory.REG.read(self.currentInstruction.A_int)-self.memory.REG.read(self.currentInstruction.B_int)
            w = BinLib.fromTwoComp(BinLib.toTwoComp(q))
            if not q == w:
                self.scheduleIntrrupt(3) #Underflow
            self.memory.REG.write(self.currentInstruction.C_int,w)
        elif self.currentInstruction.op_int == IS.OR:
            q = self.memory.REG.read(self.currentInstruction.A_int) | self.memory.REG.read(self.currentInstruction.B_int)
            self.memory.write(self.currentInstruction.C_int,q)
        elif self.currentInstruction.op_int == IS.AND:
            q = self.memory.REG.read(self.currentInstruction.A_int) & self.memory.REG.read(self.currentInstruction.B_int)
            self.memory.write(self.currentInstruction.C_int,q)    
        elif self.currentInstruction.op_int == IS.XOR:
            q = self.memory.REG.read(self.currentInstruction.A_int) ^ self.memory.REG.read(self.currentInstruction.B_int)
            self.memory.write(self.currentInstruction.C_int,q)     
        elif self.currentInstruction.op_int == IS.MOVE:
            self.memory.REG.write(self.currentInstruction.C_int, self.memory.REG.read(self.currentInstruction.A_int))
        elif self.currentInstruction.op_int == IS.PUSH:
            try:
                self.memory.Stack.push(self.memory.REG.read(self.currentInstruction.A_int))  
            except:
                self.scheduleIntrrupt(1) #Overflow Data Stack
        elif self.currentInstruction.op_int == IS.POP:
            try:
                self.memory.REG.write(self.currentInstruction.C_int,self.memory.Stack.pop()  )
            except:
                self.scheduleIntrrupt(2) #Data Stack Underflow
        elif self.currentInstruction.op_int == IS.ITT:
            self.intrupptTimer[self.currentInstruction.AB] = self.currentInstruction.C_int
        elif self.currentInstruction.op_int == IS.ITS:
            self.intrupptTable[self.currentInstruction.AB] = self.currentInstruction.second.AsAddress
            if self.currentInstruction.second:
                self.intrupptTable[self.currentInstruction.AB] = self.currentInstruction.second.AsAddress
            else:
                self.intrupptTable[self.currentInstruction.AB] = self.memory.REG.read(self.currentInstruction.C_int)

        elif self.currentInstruction.op_int == IS.SET:
            self.memory.REG.write(self.currentInstruction.C_int, self.currentInstruction.second.AsAddress)
        elif self.currentInstruction.op_int == IS.LOAD:
            if self.currentInstruction.second:
                self.memory.REG.write(self.currentInstruction.C_int,self.memory.RAM.read(self.currentInstruction.second.AsAddress))
            else:
                #print self.currentInstruction.C_int,self.memory.REG.read(self.currentInstruction.A_int),self.memory.RAM.read(3)
                self.memory.REG.write(self.currentInstruction.C_int,self.memory.RAM.read(self.memory.REG.read(self.currentInstruction.A_int)))

        elif self.currentInstruction.op_int == IS.STORE:
            
            if self.currentInstruction.second:
                #print "STORED"
                self.memory.RAM.write(self.currentInstruction.second.AsAddress,self.memory.REG.read(self.currentInstruction.A_int))
            else:
                #print "STORE"
                self.memory.RAM.write(self.memory.REG.read(self.currentInstruction.C_int),self.memory.REG.read(self.currentInstruction.A_int))
                
        elif self.currentInstruction.op_int == IS.IF:
            a = self.memory.REG.read(self.currentInstruction.A_int)
            b = self.memory.REG.read(self.currentInstruction.B_int)
            flag = self.currentInstruction.C_int
            if flag == 1:
                if a == b:
                    self.PC = self.currentInstruction.second.AsAddress -1
            elif flag == 2:
                if a > b:
                    self.PC = self.currentInstruction.second.AsAddress - 1        
            elif flag == 3:
                if a >= b:
                    self.PC = self.currentInstruction.second.AsAddress - 1
            elif flag == 4:
                if a < b:
                    self.PC = self.currentInstruction.second.AsAddress - 1
            elif flag == 5:
                if a <= b:
                    self.PC = self.currentInstruction.second.AsAddress - 1
            
        elif self.currentInstruction.op_int == IS.Return:
            if self.currentInstruction.A_int == 1:
                raise Exception
            elif self.inIntruppt:
                self.memory.REG.importREG(self.tempRegs)    
                self.inIntruppt = False
                current_int = -1
                self.PC = self.return_addr
            
    def checkIntruppts(self):
        if not self.inIntruppt:
            for x in xrange(256):
                #print self.intrupptTimer
                if self.intrupptTimer[x] == 0:
                    self.scheduleIntrrupt(x)
                    self.intrupptTimer[x] = -1
                elif not self.intrupptTimer[x] < -1:
                    self.intrupptTimer[x] -=1 
                    
            if any(self.intrupptCalled):
                for x in xrange(256):
                    if self.intrupptCalled[x] and not self.intrupptTable[x] == None :
                        current_int = x
                        self.tempRegs = self.memory.REG.exportREG()
                        self.intrupptCalled[x] = False
                        self.inIntruppt = True
                        return_addr = self.PC + 1
                        self.PC = self.intrupptTable[x]
                        break
                    elif self.intrupptCalled[x]:
                        self.intrupptCalled[x] = False
            
            