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

while True:
    screen.fill(black)
    pygame.display.update()
#____________________________________________________________________________________________________________