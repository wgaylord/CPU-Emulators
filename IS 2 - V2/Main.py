import MC2
import IS
import Memory
import time
import sys
from pluginbase import PluginBase


plugin_base = PluginBase(package='devices')
source = plugin_base.make_plugin_source(searchpath=['devices'])

mem = Memory.memory()

#mem.loadPromSudoASM("asm\Test.asm")
mem.loadPromFromBin(sys.argv[1])

cpu = MC2.cpu(mem)

devices = []


devicesEnabled = ["MemMappedScreen"]

for device_name in source.list_plugins():
    if device_name in devicesEnabled:
        device = source.load_plugin(device_name)
        exec("device = device."+device_name+"()")
        devices.append(device)

def tickDevices(cpu,devices):
    for device in devices:
        if device.currentTick == device.TickTime:
            intrupt = device.tick(cpu.memory.RAM,cpu.memory.PROM)
            device.currentTick = 0
            if intrupt:
                cpu.scheduleIntrrupt(intrupt)
        else:
            device.currentTick +=1

while not cpu.memory.PROM.read(cpu.PC).raw == IS.Instruction('0000','0000','0000','0000').raw:
    cpu.fetchIS()
    #time.sleep(.01)
    cpu.execute()
    #print cpu.memory.REG.exportREG()
    tickDevices(cpu,devices)
    cpu.checkIntruppts()
    cpu.PC = cpu.PC + 1

for device in devices:
    device.CleanUp()