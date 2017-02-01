import CPU.Core
import MotherBoard.PROM as PROM
import MotherBoard.RAM
import time
import sys
from pluginbase import PluginBase
import timeit


Prom = PROM.PROM(size = (2**16)-1)
Ram = MotherBoard.RAM.RAM((2**16)-1)

plugin_base = PluginBase(package='devices')
source = plugin_base.make_plugin_source(searchpath=['devices'])

Prom.loadPromFromBin(sys.argv[1])

delay = 0
try:
    delay = float(sys.argv[2])
except:
    pass

cpu = CPU.Core.CoreX(Prom,Ram)

run = True

devicesEnabled = ["Ports"]

devices = []

for device_name in source.list_plugins():
    if device_name in devicesEnabled:
        device = source.load_plugin(device_name)
        exec("device = device."+device_name+"()")
        devices.append(device)

def tickDevices(CPU):
    for device in devices:
        if device.currentTick == device.TickTime:
            returns = device.tick(CPU.PORTS,cpu.PROM)
            device.currentTick = 0
            if returns:
                try:
                    CPU.PORTS = returns[0]
                except:
                    pass
                try:
                    cpu.causeint(returns[1],0)
                except:
                    pass

        else:
            device.currentTick +=1

while run:
    try:
        pass
    except KeyboardInterrupt:
        run = False
    time.sleep(delay)
    #time.sleep(0.999970132)
    cpu.decode()
    try:
        cpu.execute()
    except Exception as e:
        run = False
        print e
    cpu.runINT()
    tickDevices(cpu)
    #print cpu.PC

