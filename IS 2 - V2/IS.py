import BinLib

ADD    = 0
ADDi   = 1
SUB    = 2
OR     = 3
AND    = 4
XOR    = 5
SET    = 6
MOVE    = 7
LOAD   = 8
STORE  = 9
STACK   = 10
SHIFT    = 11
IF     = 12
ITS    = 13
ITT    = 14
Return = 15


Requires2Lines = [SET,LOAD,STORE,IF,ITS]


str2OP = {"ADD":0,"ADDI":1,"SUB":2,"OR":3,"AND":4,"XOR":5,"SET":6,"MOVE":7,"LOAD":8,"STORE":9,"STACK":10,"SHIFT":11,"IF":12,"ITS":13,"ITT":14,"Return":15}

class Instruction:
    
    def __init__(self,OP,A,B,C):
        self.op = OP
        self.A = A
        self.B = B
        self.C = C
        self.raw = OP +" " +A+" "+B+" "+C
        self.op_int = int(OP,2)
        self.A_int = int(A,2)
        self.B_int = int(B,2)
        self.C_int = int(C,2)
        self.second = None
        
        self.AB = int(A+B,2)
        self.AsAddress = int(OP + A + B + C,2)
        self.AsNumber = BinLib.fromTwoComp(OP + A + B + C)
        
    def isMutliPart(self):
        if self.op_int in Requires2Lines and (self.op_int == STORE or self.op_int == LOAD):
            if self.B_int == 1:
                return False
        if self.op_int in Requires2Lines and (self.op_int == ITS):
            if self.C_int > 0:
                return False
        return self.op_int in Requires2Lines
    def __repr__(self):
        return "OP: "+ self.op +" A: " +self.A+" B: "+self.B+" C: "+self.C