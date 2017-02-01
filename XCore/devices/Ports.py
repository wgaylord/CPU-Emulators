import pygame
from PIL import Image
import time
import MotherBoard.util as util
from threading import Thread


buffer = Image.new("RGB",(16,16),"black")
running = True
ports = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0}
def screen():
    global buffer
    global running
    pygame.init()

    screen = pygame.display.set_mode((640,640))
    clock = pygame.time.Clock()

    while running:
        #clock.tick(10)
        for x in xrange(16):
        # print RAM[x],ram.read(RAM[x])
            q = util.mybin(ports[x])

            for y in xrange(16):
                buffer.putpixel((y, x), (255 * int(q[y]), 255 * int(q[y]), 255 * int(q[y])))
        t = buffer.resize((640,640)).tobytes()
        img=pygame.image.frombuffer(t,(640,640),"RGB")
        screen.blit(img,(0,0))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

class Ports:
    def __init__(self):
        self.TickTime = 0
        self.currentTick = 0
        self.screenThread = Thread(target=screen)
        self.screenThread.start()
        print("Initalizing pygame.")
        time.sleep(1)

    def tick(self, port, prom):
        global ports
        ports = port
        if running == False:
            quit()

    def CleanUp(self):
        pass