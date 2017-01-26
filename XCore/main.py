import CPU.Core
import MotherBoard.PROM
import MotherBoard.RAM

Prom = MotherBoard.PROM.PROM(size = (2**16)-1)
Ram = MotherBoard.RAM.RAM((2**16)-1)

Prom.loadPromFromBin("test.bin")

cpu = CPU.Core.CoreX(Prom,Ram)

run = True

def HandlePorts(ports):
    print ports[0]
    return ports

while run:
    try:
        pass
    except KeyboardInterrupt:
        run = False

    cpu.decode()
    #print cpu.instruction.op_int,cpu.instruction.a_int,cpu.instruction.b_int,cpu.instruction.c_int
    try:
        cpu.execute()
    except Exception as e:
        run = False
        print e
    cpu.runINT()
    cpu.PORTS = HandlePorts(cpu.PORTS)
    #print cpu.PC

