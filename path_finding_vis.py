import pygame
from pygame.locals import *
from math import *

pygame.init()
screen=pygame.display.set_mode()

black=(0,0,0)
white=(255,255,255)
gray=(125,125,125)
red=(255,0,0)
green=(0,255,0)

def write(text,des,size=50,color=white):
    font=pygame.font.SysFont(None,size)
    img=font.render(text,True,color)
    screen.blit(img,des)

height=screen.get_height()
width=screen.get_width()

def distance(a,b):
    x=a[0]
    y=a[1]
    x0=b[0]
    y0=b[1]
    
    return sqrt((x-x0)**2+(y-y0)**2)

class Button:
    def __init__(self,rect,color=white):
        self.rect=(rect[0]+2,rect[1]+2,rect[2]-4,rect[3]-4)
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

class Node:
    def __init__(self,pos,rad,id):
        self.pos=pos
        self.rad=rad
        self.id=id
        self.next=[]
        self.pre=[]
        self.data=False
        self.previous=None
    
    def connect(self,node):
        if self not in node.pre:
            node.pre.append(self)
        
        if node not in self.next:
            self.next.append(node)
    
    def disconnect(self,node):
        for i in range(len(self.next)):
            if self.next[i]==node:
                self.next.pop(i)
                break
        
        for i in range(len(node.pre)):
            if node.pre[i]==self:
                node.pre.pop(i)
                break
    
    def clear(self):
        next=self.next
        for i in next:
            self.disconnect(i)
        
        pre=self.pre
        for i in pre:
            i.disconnect(self)
    
    def paint(self):
        color=gray
        if self.data:
            color=white
        pygame.draw.circle(screen,color,self.pos,self.rad)
        
        for i in self.next:
            pygame.draw.line(screen,gray,self.pos,i.pos,3)

nodes=[]
selected=None
finger=False
id=0

add=Button((0,height-width/8,width/8,width/8))
delete=Button((width/8,height-width/8,width/8,width/8))
wire=Button((width/4,height-width/8,width/8,width/8))
type=Button((width/8*3,height-width/8,width/8,width/8))
start=Button((width/8*7,height-width/8,width/8,width/8))

wire_mode=False
wire_type=True

start_search=False
ss=0

begin=None
target=None
searched=[]
front=[]

done_search=False
tt=0

path=[]

while True:
    screen.fill(black)
    
    add.run()
    start.run()
    
    if (add.pressed)&(not add.one):
        node=Node((width/2,height/2),40,id)
        nodes.append(node)
        id+=1
        add.one=True
    
    elif not add.pressed:
        add.one=False
    
    if (start.pressed)&(not start.one):
        start_search=not start_search
        if not start_search:
            begin=None
            target=None
        start.one=True
    
    elif not start.pressed:
        start.one=False
    
    for i in nodes:
        i.paint()
    
    for i in pygame.event.get():
        pos=pygame.mouse.get_pos()
        
        if pos[1]>height-width/4:
            break
            
        if i.type==MOUSEBUTTONDOWN:
            found=False
            for j in nodes:
                dis=distance(pos,j.pos)
                if dis<=j.rad:
                    if wire_mode:
                        if wire_type:
                            selected.connect(j)
                        
                        elif not wire_type:
                            selected.disconnect(j)
                        
                    elif not wire_mode:
                        finger=True
                        selected=j
                        
                        if start_search:
                            if not begin:
                                begin=j
                            
                            elif not target:
                                target=j
                    
                    found=True
                    break
            
            if not found:
                selected=None
                wire_mode=False
                wire_type=False
        
        elif i.type==MOUSEMOTION:
            if (finger)&(bool(selected)):
                selected.pos=pos
    
        elif i.type==MOUSEBUTTONUP:
            finger=False
    
    if selected:
        pygame.draw.circle(screen,green,selected.pos,selected.rad+2,3)
        write("node id : "+str(selected.id),(20,20),60)
        
        delete.run()
        
        if delete.pressed:
            selected.clear()
            for i in range(len(nodes)):
                if nodes[i]==selected:
                    nodes.pop(i)
                    break
            
            if begin==selected:
                begin=None
            
            if target==selected:
                target=None
            
            selected=None
    
        wire.run()
        
        if (wire.pressed)&(not wire.one):
            wire_mode=not wire_mode
            wire.one=True
    
        elif not wire.pressed:
            wire.one=False
        
        if wire_mode:
            write("wire type : "+str(wire_type),(20,80),60)
            
            type.run()
            
            if (type.pressed)&(not type.one):
                wire_type=not wire_type
                type.one=True
    
            elif not type.pressed:
                type.one=False
    
    if start_search:
        if (bool(begin))&(bool(target))&(not done_search):
            pygame.draw.circle(screen,red,begin.pos,begin.rad)
            pygame.draw.circle(screen,green,target.pos,target.rad)
            
            if (0<=ss<10):
                write("searching",(20,140),60)
        
            elif (10<=ss<20):
                write("searching.",(20,140),60)
        
            elif (20<=ss<30):
                write("searching..",(20,140),60)
        
            else :
                write("searching...",(20,140),60)
        
            if ss<40:
                ss+=0.5
        
            else :
                ss=0
            
            if (not done_search)&(tt==100):
                if len(front)==0:
                    front.append(begin)
                
                if len(front)>0:
                    for i in front:
                        if target==i:
                            done_search=True
                        
                        else :
                            searched.append(i)
                            i.data=True
                    
                    new_front=[]
                    for i in front:
                        for j in i.next:
                            if j not in searched:
                                new_front.append(j)
                                j.previous=i
                    
                    front=[]
                    for i in new_front:
                        front.append(i)
            
            if tt<100:
                tt+=1
            
            elif tt>=100 :
                tt=0
            
            if done_search:
                for i in nodes:
                    i.data=False
                
                while target!=begin:
                    path.append(target)
                    target=target.previous
                
                for i in path:
                    i.data=True
                
                begin.data=True
                
        elif not begin:
            write("select a start point",(20,140))
        
        elif not target:
            pygame.draw.circle(screen,red,begin.pos,begin.rad)
            write("select a target point",(20,140))
    
    pygame.display.update()
#____________________________________________________________________________________________________________