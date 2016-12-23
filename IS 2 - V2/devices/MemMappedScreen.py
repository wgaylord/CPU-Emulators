import pygame
import BinLib
from PIL import Image
from threading import Thread

RAM = [16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]

"""
RAM for screen
Memory mapped each cell is one row of pixels
"""

buffer = Image.new("RGB",(16,16),"black")
running = True    
def screen():
    global buffer
    global running
    pygame.init()

    screen = pygame.display.set_mode((640,640))
    
    while running:
        t = buffer.resize((640,640)).tobytes()
        img=pygame.image.frombuffer(t,(640,640),"RGB")
        screen.blit(img,(0,0))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
    

class MemMappedScreen:
    def __init__(self):
        self.screenThread = Thread(target=screen)
        self.screenThread.start()
    def tick(self,ram,prom):
        
        for x in xrange(0,16):
            #print RAM[x],RAM[x+1]
            q = BinLib.toTwoComp(ram.read(RAM[x]))
            
            for y in xrange(16):
                buffer.putpixel((x,y),(255*int(q[y]),255*int(q[y]),255*int(q[y])))
            
        if not running:
            exit()
    def CleanUp(self):
        pass