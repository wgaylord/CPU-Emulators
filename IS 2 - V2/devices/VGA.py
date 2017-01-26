import pygame
import BinLib
from PIL import Image
import time
from threading import Thread

RAM = [33,34]
#      ##     Command
#         ##  Send and also ACK


#[0000000000000000]
# #####              X Pixel Address
       #####         Y Pixel Address
#           ##       R
#             ##     G
#               ##   B 
#
#Uses positive numbers and a bit mask to make setting easier.

#On sucesful set it returns 0.

           

buffer = Image.new("RGB",(25,25),"black")
running = True    
def screen():
    global buffer
    global running
    pygame.init()

    screen = pygame.display.set_mode((512,512))
    while running:
        t = buffer.resize(512,512).tobytes()
        img=pygame.image.frombuffer(t,(512,512),"RGB")
        screen.blit(img,(0,0))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

class VGA:
    def __init__(self):
        self.TickTime = 0
        self.currentTick = 0
        self.screenThread = Thread(target=screen)
        self.screenThread.start()
        print("Initalizing pygame.")
        time.sleep(.5)
        
    def tick(self,ram,prom):
        if ram.read(RAM[1]) == 1:
            Data = BinLib.toTwoComp(ram.read(RAM[0]))
            X = int(Data[:5],2)
            Y = int(Data[5:10],2)
            R = int(Data[10:12],2)
            G = int(Data[12:14],2)
            B = int(Data[14:],2)
            buffer.putpixel((X,Y),(R*63,(G*63),(B*63)))
            ram.write(Ram[1],0)
    def CleanUp(self):
        pass
        