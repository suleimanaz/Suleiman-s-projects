import pygame
from pygame.locals import *
from math import *

pygame.init()
screen=pygame.display.set_mode()

white=(255,255,255)
black=(0,0,0)
gray=(125,125,125)

def write( text , dest , size=50 , color=white ):
    font=pygame.font.SysFont(None,size)
    img=font.render(text,True,color)
    screen.blit(img,dest)

def distance(a,b):
    x=a[0]
    y=a[1]
    x0=b[0]
    y0=b[1]
    return sqrt((x-x0)**2+(y-y0)**2)

class Button():
    def __init__(self,rect,color=white):
        self.init_color=color
        
        self.rect=rect
        self.color=color
        self.pressed=False
        self.one=False
    
    def check(self):
        pressed=pygame.mouse.get_pressed()[0]
        
        if pressed:
            pos=pygame.mouse.get_pos()
            if (self.rect[0]<pos[0]<self.rect[0]+self.rect[2])&(self.rect[1]<pos[1]<self.rect[1]+self.rect[3]):
                self.pressed=True
            
            else :
                self.pressed=False
        
        else :
            self.pressed=False
    
    def paint(self):
        if self.pressed:
            r=self.init_color[0]*0.5
            g=self.init_color[1]*0.5
            b=self.init_color[2]*0.5
            self.color=(r,g,b)
        
        else :
            r=self.init_color[0]
            g=self.init_color[1]
            b=self.init_color[2]
            self.color=(r,g,b)
        
        rect=(self.rect[0]+2,self.rect[1]+2,self.rect[2]-4,self.rect[3]-4)
        pygame.draw.rect(screen,self.color,rect,0,20)
    
    def run(self):
        self.check()
        self.paint()

class Node:
    type="node"
    def __init__(self,pos,rad,id):
        self.pos=pos
        self.rad=rad
        self.id=id
        self.data=False
        self.next=[]
        self.pre=[]
    
    def connect(self,node):
        if node!=self:
            if node not in self.next:
                self.next.append(node)
        
            if self not in node.pre:
                node.pre.append(self)
    
    def disconnect(self,node):
        i=0
        while i<len(self.next):
            if self.next[i]==node:
                self.next.pop(i)
                break
            i+=1
        
        i=0
        while i<len(node.pre):
            if node.pre[i]==self:
                node.pre.pop(i)
                break
            i+=1
    
    def disconnect_all(self):
        next=[]
        for i in self.next:
            next.append(i)
        
        pre=[]
        for i in self.pre:
            pre.append(i)
        
        for i in next:
            self.disconnect(i)
        
        for i in pre:
            i.disconnect(self)
    
    def run(self):
        pass
    
    def paint(self):
        color=white
        if not self.data:
            color=gray
        
        pygame.draw.circle(screen,color,self.pos,self.rad)
        
        for i in self.next:
            pygame.draw.line(screen,color,self.pos,i.pos,3)

class Not(Node):
    type="not"
    def run(self):
        self.data=True
        for i in self.pre:
            if i.data:
                self.data=False
                break

class Buff(Node):
    type="buff"
    def run(self):
        self.data=False
        for i in self.pre:
            if i.data:
                self.data=True
                break

def new_a_nodes(nodes):
    a=[]
    for i in nodes:
        if len(i.pre)==0:
            a.append(i)
    
    return a

nodes=[]
a_nodes=[]
run_nodes=[]
selected=None
id=0
wire_mode=False
finger=False
run_mode=False
add_mode=False

add_node=Button((0,1340,100,100))
change=Button((620,1340,100,100))
wire=Button((520,1340,100,100))
con=Button((420,1340,100,100))
discon=Button((320,1340,100,100))
delete=Button((220,1340,100,100))
run=Button((100,1340,120,100))
node=Button((0,1240,100,100))
add_not=Button((100,1240,100,100))
add_buff=Button((200,1240,100,100))

while True:
    screen.fill(black)
    
    add_node.run()
    run.run()
    
    if (add_node.pressed)&(not add_node.one):
        add_mode=not add_mode
        add_node.one=True
    
    elif not add_node.pressed:
        add_node.one=False
    
    if (run.pressed)&(not run.one):
        run_mode=not run_mode
        run.one=True
    
    elif not run.pressed:
        run.one=False
    
    for i in nodes:
        i.paint()
    
    if selected:
        pygame.draw.circle(screen,(0,255,0),selected.pos,selected.rad+2,6)
        write("node id : "+str(selected.id),(0,0))
        write("node type : "+str(selected.type),(0,50))
        
        change.run()
        wire.run()
        delete.run()
        
        if (change.pressed)&(not change.one):
            selected.data=not selected.data
            change.one=True
    
        elif not change.pressed:
            change.one=False
        
        if (wire.pressed)&(not wire.one):
            if not wire_mode:
                wire_mode=3
            
            elif wire_mode:
                wire_mode=False
            
            wire.one=True
    
        elif not wire.pressed:
            wire.one=False
        
        if wire_mode:
            con.run()
            discon.run()
            
            if con.pressed:
                wire_mode=1
            
            if discon.pressed:
                wire_mode=2
        
        if (delete.pressed)&(not delete.one):
            selected.disconnect_all()
            i=0
            while i<len(nodes):
                if selected==nodes[i]:
                    nodes.pop(i)
                    break
                i+=1
            
            i=0
            while i<len(run_nodes):
                if selected==run_nodes[i]:
                    run_nodes.pop(i)
                    break
                i+=1
            
            a_nodes=new_a_nodes(nodes)
            selected=None
            wire_mode=False
            delete.one=True
        
        elif not delete.pressed:
            delete.one=False
    
    if add_mode:
        
        node.run()
        add_not.run()
        add_buff.run()
        
        if (node.pressed)&(not node.one):
            n=Node((360,720),25,id)
            id+=1
            nodes.append(n)
            a_nodes=new_a_nodes(nodes)
            node.one=True
    
        elif not node.pressed:
            node.one=False
        
        if (add_not.pressed)&(not add_not.one):
            n=Not((360,720),25,id)
            id+=1
            nodes.append(n)
            a_nodes=new_a_nodes(nodes)
            add_not.one=True
    
        elif not add_not.pressed:
            add_not.one=False
        
        if (add_buff.pressed)&(not add_buff.one):
            n=Buff((360,720),25,id)
            id+=1
            nodes.append(n)
            a_nodes=new_a_nodes(nodes)
            add_buff.one=True
    
        elif not add_buff.pressed:
            add_buff.one=False
        
    for i in pygame.event.get():
        pos=pygame.mouse.get_pos()
        if pos[1]<1240:
            if i.type==MOUSEBUTTONDOWN:
                finger=True
                found=None
                for j in nodes:
                    dis=distance(pos,j.pos)
                    if dis<=j.rad:
                        found=j
                        break
                
                if found:
                    if selected:
                        if not wire_mode:
                            selected=found
                        
                        elif wire_mode:
                            if wire_mode==1:
                                selected.connect(found)
                                a_nodes=new_a_nodes(nodes)
                            
                            elif wire_mode==2:
                                selected.disconnect(found)
                                a_nodes=new_a_nodes(nodes)
                        
                    elif not selected:
                        selected=found
                    
                elif not found:
                    selected=None
                    wire_mode=False
            
            elif i.type==MOUSEMOTION:
                if (bool(selected))&(bool(finger)):
                    selected.pos=pos
            
            elif i.type==MOUSEBUTTONUP:
                finger=False
    
    if run_mode:
        if len(run_nodes)==0:
            for i in a_nodes:
                run_nodes.append(i)
        
        new=[]
        for i in run_nodes:
            i.run()
            if len(i.next):
                for j in i.next:
                    if j not in new:
                        new.append(j)
                
            else :
                for j in a_nodes:
                    if j not in new:
                        new.append(j)
        
        run_nodes=[]
        for i in new:
            run_nodes.append(i)
    
    pygame.display.update()
#___________________________________________________________________________________________________________________________
