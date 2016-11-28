import MC2
import IS
import Memory
import time
from pluginbase import PluginBase


plugin_base = PluginBase(package='devices')
source = plugin_base.make_plugin_source(searchpath=['devices'])

mem = Memory.memory()

mem.loadProm("Test.asm")

cpu = MC2.cpu(mem)

devices = []


devicesEnabled = ["RamUsage"]

for device_name in source.list_plugins():
    if device_name in devicesEnabled:
        device = source.load_plugin(device_name)
        exec("device = device."+device_name+"()")
        
        devices.append(device)

def tickDevices(cpu,devices):
    for device in devices:
        intrupt = device.tick(cpu.memory.RAM)
        if intrupt:
            cpu.scheduleIntrrupt(intrupt)

while not cpu.memory.PROM.read(cpu.PC).raw == IS.Instruction('0000','0000','0000','0000').raw:
    #print cpu.PC
    #print cpu.memory.REG.exportRegs()
    cpu.fetchIS()
    #cpu.execute()
    try:
        cpu.execute()
    except Exception as e:
        print e
        print "Halted!"
        exit()

    tickDevices(cpu,devices)
    cpu.checkIntruppts()
    cpu.PC = cpu.PC + 1
