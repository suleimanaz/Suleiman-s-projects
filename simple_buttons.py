import pygame
from pygame.locals import *

pygame.init()
screen=pygame.display.set_mode()

black=(0,0,0)
white=(255,255,255)

def write(text,des,size=50,color=white):
    font=pygame.font.SysFont(None,size)
    img=font.render(text,True,color)
    screen.blit(img,des)

height=screen.get_height()
width=screen.get_width()

class Button:
    def __init__(self,rect,color=white):
        self.rect=rect
        self.color=color
        self.init_color=color
        self.pressed=False
        self.one=False
    
    def update(self):
        self.color=self.init_color
        if self.pressed:
            r=self.init_color[0]*0.5
            g=self.init_color[1]*0.5
            b=self.init_color[2]*0.5
            self.color=(r,g,b)
    
    def paint(self):
        pygame.draw.rect(screen,self.color,self.rect,0,20)
    
    def check(self):
        self.pressed=False
        if pygame.mouse.get_pressed()[0]:
            pos=pygame.mouse.get_pos()
            if (self.rect[0]<pos[0]<self.rect[0]+self.rect[2])&(self.rect[1]<pos[1]<self.rect[1]+self.rect[3]):
                self.pressed=True
        
    def run(self):
        self.check()
        self.update()
        self.paint()
        return self.pressed

button=Button((width/2-100,height/2-100,200,200))

while True:
    screen.fill(black)
    
    button.run()
    
    pygame.display.update()
#________________________________________________________    ____________________________________________________