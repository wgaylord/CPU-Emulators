from MotherBoard import util

int2op = {0: 'NOP', 1: 'ADD', 2: 'ADC', 3: 'SUB', 4: 'AND', 5: 'OR', 6: 'XOR', 7: 'JMP', 8: 'IO', 9: 'SFT', 10: 'SET',
          11: 'MOV', 12: 'SRM', 13: 'SMR', 14: 'RIT', 15: 'INT'}

op2int = {'NOP': 0, 'ADD': 1, 'ADC': 2, 'SUB': 3, 'AND': 4, 'OR': 5, 'XOR': 6, 'JMP': 7, 'IO': 8, 'SFT': 9, 'SET': 10,
          'MOV': 11, 'SRM': 12, 'SMR': 13, 'RIT': 14, 'INT': 15}

class Instruction():
        def __init__(self,num=0,next = 0):
            self.value = num
            #print bin(num)
            self.bin = util.format2(num)
            self.op = self.bin[:4]
            self.a = self.bin[4:8]
            self.b = self.bin[8:12]
            self.c = self.bin[12:]

            self.op_int = int(self.op, 2)
            self.a_int = int(self.a,2)
            self.b_int = int(self.b, 2)
            self.c_int = int(self.c, 2)
            self.next = util.myint(util.format2(next))

