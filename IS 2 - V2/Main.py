import MC2
import IS
import Memory
import time
from pluginbase import PluginBase


plugin_base = PluginBase(package='devices')
source = plugin_base.make_plugin_source(searchpath=['devices'])

mem = Memory.memory()

mem.loadProm("asm\Test.asm")

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
        intrupt = device.tick(cpu.memory.RAM,cpu.memory.PROM)
        if intrupt:
            cpu.scheduleIntrrupt(intrupt)

while not cpu.memory.PROM.read(cpu.PC).raw == IS.Instruction('0000','0000','0000','0000').raw:
    cpu.fetchIS()
    time.sleep(.1)
    cpu.execute()
    
    tickDevices(cpu,devices)
    cpu.checkIntruppts()
    cpu.PC = cpu.PC + 1

for device in devices:
    device.CleanUp()