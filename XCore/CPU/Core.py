import IS
import REG
import MotherBoard.util as util

class CoreX:
    def __init__(self,Prom,RAM):
        self.PROM = Prom
        self.RAM = RAM
        self.REG = REG.REG(16)
        self.PORTS = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0}
        self.INTRUPTS = {}
        self.INTTable = {}
        self.REGCopy = None
        self.inINT = False
        self.instruction = None

        self.PC = 0

    def decode(self):
        try:
            self.instruction = IS.Instruction(self.PROM.read(self.PC),self.PROM.read(self.PC+1))
        except:
            self.instruction = IS.Instruction(self.PROM.read(self.PC),0)
    def causeint(self,num,time = 0):
        self.INTRUPTS[num] = time

    def runINT(self):
        for x in self.INTRUPTS.keys():
            if self.INTRUPTS[x] == 0:
                try:
                    self.INTTable[x]
                    self.REGCopy = self.REG
                    self.inINT = True
                    self.INTRUPTS[x] = -1
                    self.oldPC = self.PC
                    self.PC = self.INTTable[x]
                except:
                    pass
            elif not self.INTRUPTS[x] == -1:
                self.INTRUPTS[x] -=1

    def execute(self):
        op = self.instruction.op_int
        a = self.instruction.a_int
        b = self.instruction.b_int
        c = self.instruction.c_int

        if op == 0: #NOP
            if self.inINT:
                self.inINT = False
                self.REG = self.REGCopy
                self.REGCopy = None
                self.PC = self.oldPC

            if a > 0 or b > 0 or c >0:
                raise Exception("HALT!")
        elif op == 1: #ADD
            temp = self.REG.read(a) + self.REG.read(b)
            if temp >= 2**15 or temp <= -(2**15):
                temp = util.rollover(temp)
                self.causeint(0)
            self.REG.write(c,temp)
        elif op == 2: #ADC
            temp = self.REG.read(a) + self.REG.read(b) + 1
            if temp >= 2 ** 15 or temp <= -(2 ** 15):
                temp = util.rollover(temp)
                self.causeint(0)
            self.REG.write(c, temp)
        elif op == 3: #SUB
            temp = self.REG.read(a) - self.REG.read(b)
            if temp >= 2 ** 15 or temp <= -(2 ** 15):
                temp = util.rollover(temp)
                self.causeint(1)
            self.REG.write(c, temp)
        elif op == 4: #AND
            temp = self.REG.read(a) & self.REG.read(b)
            self.REG.write(c, temp)
        elif op == 5: #OR
            temp = self.REG.read(a) | self.REG.read(b)
            self.REG.write(c, temp)
        elif op == 6: #XOR
            temp = self.REG.read(a) ^ self.REG.read(b)
            self.REG.write(c, temp)
        elif op == 7: #JMP
            equal = self.REG.read(a) == self.REG.read(b)
            greater = self.REG.read(a) > self.REG.read(b)
            less = self.REG.read(a) < self.REG.read(b)
            t = int(bin(c)[2:][-3:],2)
            y = 0
            try:
                y = int(bin(c)[2:][-4],2)
            except:
                pass
            address = self.instruction.next
            if y == 1:
                address = self.REG.read(self.instruction.next)
            if t == 0:
                self.PC = address
                return
            if t == 1:
                if equal:
                    self.PC = address
                    return
            if t == 2:
                if less:
                    self.PC = address
                    return
            if t == 3:
                if less or equal:
                    self.PC = address
                    return
            if t == 4:
                if greater:
                    self.PC = address
                    return
            if t == 5:
                if greater or equal:
                    self.PC = address
                    return
            if t == 6:
                if not equal:
                    self.PC = address
                    return
            self.PC +=1
        elif op == 8: #IO

            if c == 1:
                self.PORTS[a]=self.REG.read(b)
            elif c == 2:
                self.REG.write(b,self.PORTS[self.REG.read(a)])
            elif c == 3:
                self.PORTS[self.REG.read(a)] = self.REG.read(b)
            else:
                self.REG.write(b, self.PORTS[a])
        elif op == 9: #SFT
            if c == 1:
                self.REG.write(b,util.rotr(self.REG.read(a)))
            else:
                self.REG.write(b, util.rotl(self.REG.read(a)))
        elif op == 10: #SET
            self.REG.write(a,(self.instruction.next))
            self.PC += 1
        elif op == 11: #MOV
            self.REG.write(b,self.REG.read(a))
        elif op == 12: #SRM
            address = self.REG.read(b)
            if c == 1:
                address = self.instruction.next
                self.PC += 1
            self.RAM.write(address, self.REG.read(a))
        elif op == 13: #SMR
            address = self.REG.read(b)
            if c == 1:
                address = self.instruction.next
                self.PC += 1
            self.REG.write(a, self.RAM.read(address))
        elif op == 14: #RIT
            self.INTTable[self.REG.read(a)] = int(util.mybin(self.REG.read(b)),2)
        elif op == 15: #INT
            if c == 1:
                self.causeint(a, self.REG.read(b))
            else:
                self.causeint(a, b)
        self.PC += 1
        return
