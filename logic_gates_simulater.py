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
blue=(0,0,255)

def write(text,des,size=50,color=white):
    font=pygame.font.SysFont(None,size)
    img=font.render(text,True,color)
    screen.blit(img,des)

height=screen.get_height()
width=screen.get_width()

class Button:
    def __init__(self,rect,func,arg=[],type=True,color=white):
        self.rect=rect
        self.color=color
        self.func=func
        self.arg=arg
        self.type=type
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
        rect=(self.rect[0]+2,self.rect[1]+2,self.rect[2]-4,self.rect[3]-4)
        pygame.draw.rect(screen,self.color,rect,0,20)
    
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
        
        if self.type:
            if (self.pressed)&(not self.one):
                self.func(self.arg)
                self.one=True
            
            elif not self.pressed:
                self.one=False
        
        elif not self.type:
            if self.pressed:
                self.func(self.arg)

def distance(a,b):
    x=a[0]
    y=a[1]
    x0=b[0]
    y0=b[1]
    
    return sqrt((x-x0)**2+(y-y0)**2)

def second_degree_eq(a,b,c):
    delta=b**2-4*a*c
    
    if delta>=0:
        x0=(-b+sqrt(delta))/(2*a)
        x1=(-b-sqrt(delta))/(2*a)
        
        return x0,x1
    
    else :
        return False

def circle_line_eq(x0,y0,a,b,r):
    alpha=a-x0
    beta=b-y0
    
    if (not alpha) and (not beta) or (r<=0):
        return False
    
    else :
        a0=1
        
        if not alpha:
            b0=-2*y0
            c0=y0**2-r**2
            s=second_degree_eq(a0,b0,c0)
            
            y=s[0]
            y1=s[1]
            
            return (x0,y),(x0,y1)
        
        elif not beta:
            b0=-2*x0
            c0=x0**2-r**2
            s=second_degree_eq(a0,b0,c0)
            
            x=s[0]
            x1=s[1]
            
            return (x,y0),(x1,y0)
        
        else :
            b0=-2*x0
            c0=x0**2-(r**2/(1+beta**2/alpha**2))
            s=second_degree_eq(a0,b0,c0)
            
            x=s[0]
            x1=s[1]
            
            y=beta/alpha*(x-x0)+y0
            y1=beta/alpha*(x1-x0)+y0
            
            return (x,y),(x1,y1)

class Node:
    type='node'
    def __init__(self,pos,rad,id):
        self.pos=pos
        self.rad=rad
        self.id=id
        
        self.data=False
        self.pre=[]
    
    def connect(self,node):
        if self not in node.pre:
            node.pre.append(self)
    
    def disconnect(self,node):
        for i in range(len(node.pre)):
            if node.pre[i]==self:
                node.pre.pop(i)
                break
    
    def clear(self):
        pre=[]
        
        for i in self.pre:
            pre.append(i)
        
        for i in pre:
            i.disconnect(self)
    
    def paint(self):
        color=gray
        if self.data:
            color=white
        
        pygame.draw.circle(screen,color,self.pos,self.rad)
        
        for i in self.pre:
            if distance(self.pos,i.pos)>self.rad+i.rad:
                sol=circle_line_eq(self.pos[0],self.pos[1],i.pos[0],i.pos[1],self.rad/4*5)
                dis1=distance(i.pos,sol[0])
                dis2=distance(i.pos,sol[1])
                
                p1=sol[0]
                if dis1>dis2:
                    p1=sol[1]
                
                sol=circle_line_eq(i.pos[0],i.pos[1],self.pos[0],self.pos[1],i.rad/4*5)
                dis1=distance(self.pos,sol[0])
                dis2=distance(self.pos,sol[1])
                
                p2=sol[0]
                if dis1>dis2:
                    p2=sol[1]
                
                color=gray
                if i.data:
                    color=white
                
                pygame.draw.line(screen,color,p1,p2,int(width/200))
                pygame.draw.circle(screen,color,p1,int(width/150))

class Not(Node):
    type='not'

class Buff(Node):
    type='buff'

vis_nodes=[]
nodes=[]
vis_pos=[]

bs=width/7

adding=False
wiring=False
coning=True
runing=False

selected=None

fingerdown=False
fingerdownpos=None

id=0

def add_func(arg):
    global adding
    
    adding=not adding

def add_node_func(arg):
    global nodes
    global vis_nodes
    global id
    
    node=Node((width/2,height/2),width/30,id)
    
    nodes.append(node)
    vis_nodes.append(node)
    id+=1

def wire_func(arg):
    global wiring
    
    wiring= not wiring

def con_dis_func(arg):
    global coning
    
    coning= not coning

def delete_func(arg):
    global vis_nodes
    global nodes
    global selected
    
    selected.clear()
    
    for i in range(len(vis_nodes)) :
        if vis_nodes[i]==selected:
            vis_nodes.pop(i)
            break
    
    for i in range(len(nodes)):
        if nodes[i]==selected:
            nodes.pop(i)
            break
    
    selected=None

def add_not_func(arg):
    global nodes
    global vis_nodes
    global id
    
    node=Not((width/2,height/2),width/30,id)
    
    nodes.append(node)
    vis_nodes.append(node)
    id+=1

def add_buff_func(arg):
    global nodes
    global vis_nodes
    global id
    
    node=Buff((width/2,height/2),width/30,id)
    
    nodes.append(node)
    vis_nodes.append(node)
    id+=1

def run_func(arg):
    global runing
    
    runing=not runing

def switch_func(arg):
    global selected
    
    selected.data=not selected.data

add=Button((0,height-bs,bs,bs),add_func)
add_node=Button((0,height-2*bs,bs,bs),add_node_func)
wire=Button((bs,height-bs,bs,bs),wire_func)
con_dis=Button((bs*2,height-bs,bs,bs),con_dis_func)
delete=Button((width-2*bs,height-3*bs,bs,bs),delete_func)
add_not=Button((bs,height-2*bs,bs,bs),add_not_func)
add_buff=Button((bs*2,height-2*bs,bs,bs),add_buff_func)
run=Button((width-bs,height-3*bs,bs,bs),run_func)
switch=Button((width-bs,height-bs,bs,bs),switch_func)

while True:
    screen.fill(black)
    
    for i in vis_nodes:
        i.paint()
    
    pygame.draw.rect(screen,gray,(0,0,width,bs*3),0,20)
    pygame.draw.rect(screen,gray,(0,height-bs*3,width,bs*3),0,20)
    
    add.run()
    run.run()
    
    if adding:
        add_node.run()
        add_not.run()
        add_buff.run()
        
    for i in pygame.event.get():
        pos=pygame.mouse.get_pos()
        if bs*3<pos[1]<height-bs*3:
            if i.type==MOUSEBUTTONDOWN:
                fingerdownpos=pos
                
                vis_pos=[]
                for i in vis_nodes:
                    vis_pos.append(i.pos)
                
                found=False
                for j in vis_nodes:
                    if distance(pos,j.pos)<j.rad:
                        if not wiring:
                            fingerdown=True
                            selected=j
                        
                        elif wiring:
                            if j==selected:
                                fingerdown=True
                            
                            if coning:
                                selected.connect(j)
                            
                            elif not coning:
                                selected.disconnect(j)
                        
                        found=True
                        break
                
                if not found:
                    selected=None
            
            elif i.type==MOUSEMOTION:
                if (bool(selected))&(fingerdown):
                    selected.pos=pos
                
                elif (not selected)&(bool(fingerdownpos)):
                    for i in range(len(vis_nodes)):
                        drift=(pos[0]-fingerdownpos[0],pos[1]-fingerdownpos[1])
                        vis_nodes[i].pos=(vis_pos[i][0]+drift[0],vis_pos[i][1]+drift[1])
            
            elif i.type==MOUSEBUTTONUP:
                fingerdown=False
                fingerdownpos=None
    
    if selected:
        pygame.draw.circle(screen,green,selected.pos,selected.rad*5/4,int(selected.rad/4))
        write("node id : "+str(selected.id),(20,20),int(bs/2))
        write("node type : "+str(selected.type),(20,20+bs/2),int(bs/2))
        wire.run()
        delete.run()
        switch.run()
        
        if wiring:
            write("wiring type : "+str(coning),(20,20+bs),int(bs/2))
            con_dis.run()
    
    elif not selected:
        wiring=False
        coning=True
   
    if runing:
        write("runing",(20,20+bs/2*3),int(bs/2))
        
        new=[]
        for i in nodes:
            if i.type=="not":
                data=True
                for j in i.pre:
                    if j.data:
                        data=False
                
                new.append(data)
            
            elif i.type=="buff":
                data=False
                for j in i.pre:
                    if j.data:
                        data=True
                
                new.append(data)
            
            elif i.type=="node":
                new.append(i.data)
        
        for i in range(len(nodes)):
            nodes[i].data=new[i]
    
    pygame.display.update()
#___________________________________________________________________________________________________________