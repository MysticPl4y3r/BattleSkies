'''Sounds from freesoundeffects.com
Music and assets made using FL Studio, Piskel by Andrew Jason
Game made by Andrew Jason
Learnt from youtube channel "Tech with Tim"'''


import pygame, sys, random, math




#Variables
FPS=30
screenwidth=640
screenheight=480
t=0
T1Missile_Reserve=10
T1Ammunition=2000
score=0
ene_killed=0
pause=0
ismenu=True
isboss=False
ang=0
rev=True
ShotOnce=False
win=0

#Objects

class Reaper(object):
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.moveCount=0
        self.facecount=5
        self.steps=10
        self.left=False
        self.righ=False
        self.up=False
        self.down=False
        self.hitbox=(self.x,self.y+15,64,32)
        self.health=900
        self.visible=True
        
    def Animation(self,display):
        if self.visible:
            if self.moveCount+1>18:
                self.moveCount=0
            elif self.left:
                display.blit(Airbrakes[self.moveCount//3],(self.x,self.y))
                self.moveCount+=1
            elif self.right:
                display.blit(Afterburners[self.moveCount//3],(self.x,self.y))
                self.moveCount+=1
            elif self.up:
                display.blit(Ascent[self.moveCount//3],(self.x,self.y))
                self.moveCount+=1
            elif self.down:
                display.blit(Descent[self.moveCount//3],(self.x,self.y))
                self.moveCount+=1
            else:
                display.blit(JetNormal[self.moveCount//3],(self.x,self.y))
                self.moveCount+=1
            self.hitbox=(self.x+25,self.y+25,20,20)
            
            # pygame.draw.rect(display,(255,0,0),self.hitbox,2)
    
    
    
    def hit(self,dmg):
    
        if self.health >1:
            self.health-=dmg
            Hitmarker.play()
        if self.health<=0:
            if self.visible:
                KaBoom.play()
            self.health=0
            self.visible=False 
            
           
class _25(object):
    def __init__(self,x,y,size):
        self.x = x
        self.y = y
        self.size=size
        self.steps=12
        self.muzCount=0
    
    def gunAnimation(self,display):
        display.blit(T1bullet,(self.x,self.y))
     
    def hitmark(self,rect):
        if self.y - self.size < rect[1] + rect[3] and self.y + self.size > rect[1]:
                if self.x + self.size > rect[0] and self.x - self.size < rect[0] +rect[2]:
                    return True
        return False
            
class Missile(object):
    def __init__(self,x,y,size):
        self.x=x
        self.y=y
        self.size=size
        self.steps=17
        
    
    def missileAnimation(self,display):
        display.blit(T1missile,(self.x,self.y))
    
    def hitmark(self,rect):
        if self.y - self.size < rect[1] + rect[3] and self.y + self.size > rect[1]:
                if self.x + self.size > rect[0] and self.x - self.size < rect[0] +rect[2]:
                    return True
        return False

class MaxAmmo(object):
    def __init__(self,x,y,size):
        self.x=x
        self.y=y
        self.size=size
        self.steps=3
        self.visible=True
        self.hitbox=(self.x,self.y,32,32)
    
    def Animation(self,display):
        self.move()
        if self.visible:
            display.blit(MaxAm,(self.x,self.y))
            self.hitbox=(self.x,self.y,32,32)
            # pygame.draw.rect(display,(255,0,0),self.hitbox,2)
    
    def move(self):
        if self.x-self.steps>screenwidth*-1:
            self.x-=self.steps
    
    def hit(self):
        global T1Ammunition
        T1Ammunition=2000
    
    def collide(self,rect):
        if rect[1] < self.hitbox[1] + self.hitbox[3] and rect[1] + rect[3] > self.hitbox[1]:
             if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
                 return True
        return False      

class MaxHealth(object):
    def __init__(self,x,y,size):
        self.x=x
        self.y=y
        self.size=size
        self.steps=3
        self.visible=True
        self.hitbox=(self.x,self.y,32,32)
    
    def Animation(self,display):
        self.move()
        if self.visible:
            display.blit(MaxHeal,(self.x,self.y))
            self.hitbox=(self.x,self.y,32,32)
            # pygame.draw.rect(display,(255,0,0),self.hitbox,2)
    
    def move(self):
        if self.x-self.steps>screenwidth*-1:
            self.x-=self.steps
    
    def hit(self):
        jet.health=900
        
    
    def collide(self,rect):
        if rect[1] < self.hitbox[1] + self.hitbox[3] and rect[1] + rect[3] > self.hitbox[1]:
             if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
                 return True
        return False      

class bulletplasma(object):
    def __init__(self,x,y,radius,destx,desty):
        self.x=x
        self.y=y
        self.destx=destx
        self.desty=desty
        self.radius=radius
        self.steps=4
        self.hitbox=(self.x,self.y,self.radius)
        difx=self.destx - self.x
        dify=self.desty - self.y
        angle =math.atan2(dify,difx)
        self.chx = math.cos(angle) * self.steps
        self.chy = math.sin(angle) * self.steps
    
    def Animation(self,display):
        self.move()
        
        pygame.draw.circle(display,(255,0,200),(int(self.x),int(self.y)),self.radius)
        pygame.draw.circle(display,(150,150,150),(int(self.x),int(self.y)),self.radius-1)
    
    def move(self):
        if self.x-self.steps>screenwidth*-1 and self.y-self.steps>screenheight*-1:
            self.x+=self.chx
            self.y+=self.chy
    def outofdisplay(self,width,height):
        return not (self.x <= width and self.x >= 0)
        return not (self.y <= height and self.y >= 0)
    
    def collide(self,rect):
        if self.y - self.radius < rect[1] + rect[3] and self.y + self.radius > rect[1]:
                if self.x + self.radius > rect[0] and self.x - self.radius < rect[0] + rect[2]:
                    return True
        return False
    
class Weak_Enemy(object):
    Grunt=[pygame.image.load('Textures/Grunt/GruntE0.png'),pygame.image.load('Textures/Grunt/GruntE1.png'),pygame.image.load('Textures/Grunt/GruntE2.png'),pygame.image.load('Textures/Grunt/GruntE3.png'),pygame.image.load('Textures/Grunt/GruntE4.png')]
    CLDWN=15
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.FlightCount=0
        self.steps=8
        self.hitbox=(self.x,self.y+20,64,25)
        self.health=350
        self.visible=True
        self.bullets=[]
        self.cooldown=0
        
    def Animation(self,display):
        self.move()
        if self.visible:
            if self.FlightCount+1>=15:
                self.FlightCount=0
            display.blit(self.Grunt[self.FlightCount//3],(self.x,self.y))
            self.hitbox=(self.x,self.y+20,64,25)
            # pygame.draw.rect(display,(255,0,0),self.hitbox,2)
        for bullet in self.bullets:
            bullet.Animation(display)
    
    def move_bullets(self,hitbox):
        self.cool()
        for bullet in self.bullets:
            bullet.move()
            if bullet.outofdisplay(screenwidth,screenheight):
                self.bullets.remove(bullet)
            elif bullet.collide(hitbox):
                jet.hit(70)
                self.bullets.remove(bullet)
                if not jet.visible:
                    died()
                    
    def cool(self):
        if self.cooldown>=self.CLDWN:
            self.cooldown=0
        elif self.cooldown>0:
            self.cooldown+=1
    
    def shoot(self):
        if self.cooldown==0:
          bullet=bulletplasma(self.x,self.y+39,5,jet.x+30,jet.y+30)
          self.bullets.append(bullet)
          self.cooldown=1
    
    def move(self):
        if self.x-self.steps>screenwidth*-1:
            self.x-=self.steps
            self.FlightCount+=1
    
    def hit(self,dmg):
        global ene_killed, T1Ammunition, score
        if self.health < dmg:
            self.health-=dmg
            score+=3
            if T1Ammunition<2000:
                T1Ammunition+=25
            if jet.health < 900:
                jet.health+=20
            self.visible=False
            if self.health<=0:
                ene_killed+=1

        if self.health >1:
            self.health-=dmg       
                
    def collide(self,rect):
        if rect[1] < self.hitbox[1] + self.hitbox[3] and rect[1] + rect[3] > self.hitbox[1]:
             if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
                 return True
        return False


class Normal_Enemy(object):
    Fighter=[pygame.image.load('Textures/Fighter/EnemyFighter0.png'),pygame.image.load('Textures/Fighter/EnemyFighter1.png'),pygame.image.load('Textures/Fighter/EnemyFighter2.png'),pygame.image.load('Textures/Fighter/EnemyFighter3.png'),pygame.image.load('Textures/Fighter/EnemyFighter4.png')]
    CLDWN=15
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.FlightCount=0
        self.steps=7
        self.hitbox=(self.x,self.y+20,60,23)
        self.health=500
        self.visible=True
        self.bullets=[]
        self.cooldown=0
        
    def Animation(self,display):
        self.move()
        if self.visible:
            if self.FlightCount+1>=15:
                self.FlightCount=0
            display.blit(self.Fighter[self.FlightCount//3],(self.x,self.y))
            self.hitbox=(self.x,self.y+20,60,23)
            # pygame.draw.rect(display,(255,0,0),self.hitbox,2)
        for bullet in self.bullets:
            bullet.Animation(display)
            
    def move_bullets(self,hitbox):
        self.cool()
        for bullet in self.bullets:
            bullet.move()
            if bullet.outofdisplay(screenwidth,screenheight):
                self.bullets.remove(bullet)
            elif bullet.collide(hitbox):
                jet.hit(70)
                self.bullets.remove(bullet)
                if not jet.visible:
                    died()
                    
    def cool(self):
        if self.cooldown>=self.CLDWN:
            self.cooldown=0
        elif self.cooldown>0:
            self.cooldown+=1
    
    def shoot(self):
        if self.cooldown==0:
          bullet=bulletplasma(self.x,self.y+32,5,jet.x+30,jet.y+30)
          self.bullets.append(bullet)
          self.cooldown=1
    
    def move(self):
        if self.x-self.steps>screenwidth*-1:
            self.x-=self.steps
            self.FlightCount+=1
    
    def hit(self,dmg):
        global ene_killed, T1Ammunition, l_t, score
        if self.health < dmg:
            self.health-=dmg
            score+=5
            if T1Ammunition<2000:
                T1Ammunition+=200
            self.visible=False
            self.visible=False
            if self.health<=0:
                ene_killed+=1
                
        if self.health >1:
            self.health-=dmg
       
                
    def collide(self,rect):
        if rect[1] < self.hitbox[1] + self.hitbox[3] and rect[1] + rect[3] > self.hitbox[1]:
             if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
                 return True
        return False
        
class Big_Enemy(object):
    LazerEnemy=[pygame.image.load('Textures/LAZER/Rhino0.png'),pygame.image.load('Textures/LAZER/Rhino1.png'),pygame.image.load('Textures/LAZER/Rhino2.png'),pygame.image.load('Textures/LAZER/Rhino3.png'),pygame.image.load('Textures/LAZER/Rhino4.png')]
    CLDWN=15
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.FlightCount=0
        self.steps=4
        self.hitbox=(self.x,self.y+13,64,32)
        self.health=750
        self.visible=True
        self.bullets=[]
        self.cooldown=0
        
    def Animation(self,display):
        self.move()
        if self.visible:
            if self.FlightCount+1>=15:
                self.FlightCount=0
            display.blit(self.LazerEnemy[self.FlightCount//3],(self.x,self.y))
            self.hitbox=(self.x,self.y+13,64,32)
            # pygame.draw.rect(display,(255,0,0),self.hitbox,2)
        for bullet in self.bullets:
            bullet.Animation(display)
            
    def move_bullets(self,hitbox):
        self.cool()
        for bullet in self.bullets:
            bullet.move()
            if bullet.outofdisplay(screenwidth,screenheight):
                self.bullets.remove(bullet)
            elif bullet.collide(hitbox):
                jet.hit(70)
                self.bullets.remove(bullet)
                if not jet.visible:
                    died()
                    
    def cool(self):
        if self.cooldown>=self.CLDWN:
            self.cooldown=0
        elif self.cooldown>0:
            self.cooldown+=1
    
    def shoot(self):
        if self.cooldown==0:
          bullet=bulletplasma(self.x+4,self.y+27,5,jet.x+30,jet.y+30)
          self.bullets.append(bullet)
          self.cooldown=1
    
    def move(self):
        if self.x-self.steps>screenwidth*-1:
            self.x-=self.steps
            self.FlightCount+=1        
    
    def hit(self,dmg):
        global ene_killed, T1Ammunition, l_t, score
        if self.health < dmg:
            self.health-=dmg
            score+=2
            if jet.health < 900:
                jet.health+=90
            self.visible=False
            if self.health<=0:
                ene_killed+=1
                
        if self.health >1:
            self.health-=dmg
        
    def collide(self,rect):
        if rect[1] < self.hitbox[1] + self.hitbox[3] and rect[1] + rect[3] > self.hitbox[1]:
             if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
                 return True
        return False

class Boss(object):
    Bos=[pygame.image.load('Textures/Boss/EneBoss0.png'),pygame.image.load('Textures/Boss/EneBoss1.png'),pygame.image.load('Textures/Boss/EneBoss2.png'),pygame.image.load('Textures/Boss/EneBoss3.png'),pygame.image.load('Textures/Boss/EneBoss4.png')]
    CLDWN=30
    def __init__(self,x,y,width,height,destx,desty):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.FlightCount=0
        self.steps=6
        self.hitbox=(self.x,self.y+20,64,25)
        self.health=5000
        self.visible=True
        self.bullets=[]
        self.missiles=[]
        self.cooldown=0
        self.destx=destx
        self.desty=desty
        difx=self.destx - self.x
        dify=self.desty - self.y
        angle =math.atan2(dify,difx)
        self.chx = math.cos(angle) * self.steps
        self.chy = math.sin(angle) * self.steps
    
    def Animation(self,display):
        self.move()
        if self.visible:
            if self.FlightCount+1>=15:
                self.FlightCount=0
            display.blit(self.Bos[self.FlightCount//3],(self.x,self.y))
            pygame.draw.rect(display,(100,0,0),(screenwidth/2-500/2,50,500,20),2) 
            pygame.draw.rect(display,(255,0,0),(screenwidth/2-500/2,50,500 - (500/5000) * (5000 - self.health),20)) 
            self.hitbox=(self.x,self.y+20,64,25)
            # pygame.draw.rect(display,(255,0,0),self.hitbox,2)
        for bullet in self.bullets:
            bullet.Animation(display)
        for missile in self.missiles:
            missile.Animation(display)
    
    def move_bullets(self,hitbox):
        self.cool()
        for bullet in self.bullets:
            bullet.move()
            if bullet.outofdisplay(screenwidth,screenheight):
                self.bullets.remove(bullet)
            elif bullet.collide(hitbox):
                jet.hit(80)
                if not jet.visible:
                    died()
                else:
                    self.bullets.remove(bullet)
                    
        for missile in self.missiles:
            missile.move()
            if missile.outofdisplay(screenwidth,screenheight):
                self.missiles.remove(missile)
            elif missile.collide(hitbox):
                jet.hit(500)
                if not jet.visible:
                    died()
                else:
                    self.missiles.remove(missile)
    def cool(self):
        if self.cooldown>=self.CLDWN:
            self.cooldown=0
        elif self.cooldown>0:
            self.cooldown+=1
    
    
    def shoot(self,angle):
        # if self.cooldown==0:
            bullet=bossbullet(self.x,self.y+39,5,angle)
            self.bullets.append(bullet)
            # self.cooldown=1
            
    def shootM(self):
        if self.cooldown==0:
            self.cooldown=1
            miss1=bossmissile(self.x,self.y,5,jet.x+30,jet.y+30)
            self.missiles.append(miss1)
    
    def move(self):
        if self.x-self.steps>screenwidth*-1:
            if not self.x-self.steps<500:
                self.x-=self.steps
            self.FlightCount+=1
                
    def hit(self,dmg):
        global ene_killed, T1Ammunition, score
        if self.health < dmg:
            self.health-=dmg
            score+=1000
            if T1Ammunition<2000:
                T1Ammunition+=600
            if jet.health < 900:
                jet.health+=400
            self.visible=False
            if self.health<=0:
                ene_killed+=1

        if self.health >1:
            self.health-=dmg       
                
    def collide(self,rect):
        if rect[1] < self.hitbox[1] + self.hitbox[3] and rect[1] + rect[3] > self.hitbox[1]:
             if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
                 return True
        return False
    
class bossbullet(object):
    def __init__(self,x,y,radius,angle):
        self.x=x
        self.y=y
        self.radius=radius
        self.steps=3
        self.angle=angle
        self.stepsx=self.steps*math.cos(math.radians(angle)) 
        self.stepsy=self.steps*math.sin(math.radians(angle))
        self.hitbox=(self.x,self.y,self.radius)
    
    def Animation(self,display):
        self.move()
        pygame.draw.circle(display,(0,250,0),(int(self.x),int(self.y)),self.radius)
        pygame.draw.circle(display,(250,0,250),(int(self.x),int(self.y)),self.radius-1)
    
    def move(self):
        if self.x-self.steps>screenwidth*-1 and self.y-self.steps>screenheight*-1:
            self.x-=self.stepsx
            self.y-=self.stepsy
    
    def outofdisplay(self,width,height):
        return not (self.x <= width and self.x >= 0)
        return not (self.y <= height and self.y >= 0)
    
    def collide(self,rect):
        if self.y - self.radius < rect[1] + rect[3] and self.y + self.radius > rect[1]:
                if self.x + self.radius > rect[0] and self.x - self.radius < rect[0] + rect[2]:
                    return True
        return False
    
class bossmissile(object):
    bmissile=pygame.image.load('Textures/BossMissile.png')
    def __init__(self,x,y,size,destx,desty):
        self.x=x
        self.y=y
        self.size=size
        self.steps=7
        self.hitbox=(self.x,self.y,self.size)
        self.destx=destx+30
        self.desty=desty+30
        difx=self.destx - self.x
        dify=self.desty - self.y
        self.angle=math.atan2(dify,difx)
        self.chx = math.cos(self.angle) * self.steps
        self.chy = math.sin(self.angle) * self.steps
        
    def Animation(self,display):
        self.move()
        homing = pygame.transform.rotate(self.bmissile, math.degrees(-self.angle))
        # new_img = homing.get_rect(center = image.get_rect(topleft = topleft).center)
        display.blit(homing,(self.x,self.y))
        
    def move(self):
        if self.x-self.steps>screenwidth*-1 and self.y-self.steps>screenheight*-1:
            self.x+=self.chx
            self.y+=self.chy
            
    def outofdisplay(self,width,height):
        return not (self.x <= width and self.x >= 0)
        return not (self.y <= height and self.y >= 0)
        
    
    def collide(self,rect):
        if self.y - self.size < rect[1] + rect[3] and self.y + self.size > rect[1]:
                if self.x + self.size > rect[0] and self.x - self.size < rect[0] + rect[2]:
                    return True
        return False

def patt():
    global ang
    if random.randrange(0,5)==1:
            bosss.shoot(ang)
            bosss.shoot(ang+1*90)
            bosss.shoot(ang+1*45)
            bosss.shoot(ang+2*90)
            bosss.shoot(ang+3*45)
            bosss.shoot(ang+3*90)
            bosss.shoot(ang+5*45)
            bosss.shoot(ang+7*45)
            # ang+=1
            
def patte():
    global ang,rev
    if random.randrange(0,25)==1:
        for h in range(0,361):
            if h%15==0:
                bosss.shoot(h)
        for i in range(0,361):
            if i%30==0 and i%15==0:
                bosss.shoot(i)
        for j in range(0,361):
            if j%45==0 and j%30!=0 and h%15==0:
                bosss.shoot(j)
        for k in range(0,361):
            if k%60==0 and k%45!=0 and k%30!=0 and k%15==0:
                bosss.shoot(k)
        for l in range(0,361):
            if l%75==0 and l%60!=0 and l%45!=0 and l%30!=0 and l%15==0:
                bosss.shoot(l)
    if random.randrange(0,30)==1:
            bosss.shoot(ang+0*5)
            bosss.shoot(ang+1*5)
            bosss.shoot(ang+(-1)*5)
    if ang==60*(-1):
        rev=True
    elif ang>=60:
        rev=False
    if rev:
        ang+=1
    else:
        ang-=1
        
def pattm():
    global ang, rev
    if random.randrange(0,3)==1:
        # bosss.shoot(ang+1*45)
        # bosss.shoot(ang+3*45)
        bosss.shoot(ang+5*45)
        bosss.shoot(ang+7*45)
    if ang==0:
        rev=True
    elif ang>=120:
        rev=False
    if rev:
        ang+=1
    else:
        ang-=1

def patth():
    global ang, rev
    if random.randrange(0,3)==1:
        bosss.shoot(ang+1*45)
        bosss.shoot(ang+3*45)
        bosss.shoot(ang+5*45)
        bosss.shoot(ang+7*45)
    if ang==0:
        rev=True
    elif ang>=120:
        rev=False
    if rev:
        ang+=3
    else:
        ang-=3
        
def pattd():
    global ang, rev
    if random.randrange(0,30)==1:
        for h in range(0,361):
            if h%15==0:
                bosss.shoot(h)
        for i in range(0,361):
            if i%30==0 and i%15==0:
                bosss.shoot(i)
        for j in range(0,361):
            if j%45==0 and j%30!=0 and h%15==0:
                bosss.shoot(j)
        for k in range(0,361):
            if k%60==0 and k%45!=0 and k%30!=0 and k%15==0:
                bosss.shoot(k)
        for l in range(0,361):
            if l%75==0 and l%60!=0 and l%45!=0 and l%30!=0 and l%15==0:
                bosss.shoot(l)
    if random.randrange(0,3)==1:
        bosss.shoot(ang+1*45)
        bosss.shoot(ang+3*45)
        bosss.shoot(ang+5*45)
        bosss.shoot(ang+7*45)
    if ang==0:
        rev=True
    elif ang>=120:
        rev=False
    if rev:
        ang+=3
    else:
        ang-=3

def bossevent():
    BGBoss=pygame.mixer.music.load('music/Boss.mp3')
    pygame.mixer.music.set_volume(.8)
    pygame.mixer.music.play(-1)
    
def musicReload():
    pygame.mixer.music.stop()
    BGM=pygame.mixer.music.load('music/BattleSkies Theme.mp3')
    pygame.mixer.music.set_volume(.8)
    pygame.mixer.music.play(-1)
    
def died():
    global die,pause
    if not jet.visible:
        if pause==0:
            die=FPS
            pause = 1
            pygame.mixer.music.set_volume(0)

def DrawAnim(minutes,seconds):
    global S_time , l_t
    display.blit(Daytime, (0,0))
    display.blit(backdropclouds, (BGCX,0))  
    display.blit(backdropclouds, (BGCX2,0))   
    jet.Animation(display)  
    for rounds in gun_ammo:
        rounds.gunAnimation(display)
    
    # for lazer in laz:
    #     lazer.gunAnimation(display)
    
    for missile in missiles:
        missile.missileAnimation(display)
    for enemy in enemies:
        enemy.Animation(display)
    for powerUp in powerUps:
        powerUp.Animation(display)
    for bosss in bossene:
        bosss.Animation(display)
    display.blit(HUD,(0,0))
    if jet.health >=720:
        display.blit(Mugshot[0],(240,400))                        #540,390
    elif jet.health >= 450 and jet.health < 720:
        display.blit(Mugshot[1],(240,400))
    elif jet.health >= 270 and jet.health < 450:
        display.blit(Mugshot[2],(240,400))
    elif jet.health >= 90 and jet.health < 270:
        display.blit(Mugshot[3],(240,400))
    elif jet.health >= 0 and jet.health < 90:
        display.blit(Mugshot[4],(240,400))
    else:
        display.blit(Mugshot[5],(240,390))
            
    pygame.draw.rect(display,(255,255,86),(100,460,50,10),1)
    pygame.draw.rect(display,(255,255,86),(100,460,50 - (50/2000) * (2000 - T1Ammunition),10))
    
    pygame.draw.rect(display,(0,255,0),(20,460,50,10),1)
    pygame.draw.rect(display,(0,255,0),(20,460,50 - (50/900) * (900 - jet.health),10))
    GameEnd = GameOver.render('You Died!', 1 , (255,0,0))
    Scor_t = ScoreFont.render('Score: ' + str(score), 1 , (0,200,10))
    Kill_t = killcount.render('KILLS: ' + str(ene_killed), 1 , (255,0,0))
    Rocket_t=RocketCount.render(str(T1Missile_Reserve), 1 , (255,255,85))
    S_time="{0:02}:{1:02}".format(minutes, seconds)
    TIME=killcount.render(str(S_time),1,(255,200,255))
    percenthealth=int((jet.health/900)*100)
    HP=HealthPercentFont.render(str(percenthealth)+' %',1,(100,100,100))
    display.blit(TIME,(580,0))
    display.blit(Scor_t,(10,0))
    display.blit(Kill_t,(130,5))
    display.blit(Rocket_t,(200,449))
    display.blit(HP,(25,458))
    if not jet.visible:
        display.blit(GameEnd,(200,200))

    pygame.display.update()

def updateScore():
    f1=open('highscore.txt','r')
    content=f1.readlines()
    last=int(content[0])
    
    if last<int(score):
        f1.close()
        f2=open('highscore.txt','w')
        f2.write(str(score))
        f2.close()
        return score
    return last

def quitgame():
    run=True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.set_volume(.6)
                run=False
        keys=pygame.key.get_pressed()
        if keys[pygame.K_y]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_n]:
            run=False
        pygame.draw.rect(display,(100,100,100),(100,200,440,70))
        pygame.draw.rect(display,(50,50,50),(100,200,440,70),2)
        quitFont=pygame.font.SysFont('bahnschrift',20)
        Quit=quitFont.render("You can't leave yet, Humanity depends on you!",1, (255,255,80))
        conti=quitFont.render("Press N to continue",1, (50,255,50))
        display.blit(Quit, (screenwidth/2 - Quit.get_width()/2,200))
        display.blit(conti, (screenwidth/2 - conti.get_width()/2,220))
        quitter=quitFont.render("Press Y to quit",1, (255,50,50))
        display.blit(quitter, (screenwidth/2 - quitter.get_width()/2,240))
        pause=quitFont.render("Game Paused",1, (255,255,255))
        display.blit(pause, (screenwidth/2 - pause.get_width()/2,380))
        pygame.display.update()

def controls():
    run=True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run=False
        keys=pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
              run=False
        display.blit(Daytime, (0,0))
        controlFont=pygame.font.SysFont('comicsans',30)
        c1=controlFont.render("Arrow keys = movement",1, (255,255,255))
        c2=controlFont.render("Space = Shoot",1, (255,255,255))
        c3=controlFont.render("M = Missile",1, (255,255,255))
        c4=controlFont.render("ESC = Quit Game",1, (255,255,255))
        cq=controlFont.render("Backspace = Quit this window",1, (255,255,255))
        display.blit(c1, (screenwidth/2 - c1.get_width()/2,200))
        display.blit(c2, (screenwidth/2 - c2.get_width()/2,220))
        display.blit(c3, (screenwidth/2 - c3.get_width()/2,240))
        display.blit(c4, (screenwidth/2 - c4.get_width()/2,260))
        display.blit(cq, (screenwidth/2 - cq.get_width()/2,280))
        pygame.display.update()

def menu():
    global ismenu
    run=True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.set_volume(.6)
                run=False
        keys=pygame.key.get_pressed()
        if keys[pygame.K_c]:
           controls()
        if keys[pygame.K_ESCAPE]:
            quitgame()
        display.blit(Daytime, (0,0))
        helpFont=pygame.font.SysFont('comicsans',30)
        Main_menuFont=pygame.font.SysFont('bahnschrift',100)
        Prev_Score=Main_menuFont.render('BATTLESKIES',1, (255,180,230))
        display.blit(Prev_Score, (screenwidth/2 - Prev_Score.get_width()/2,200))
        play=helpFont.render("Press LMB to begin",1, (255,255,255))
        display.blit(play, (screenwidth/2 - play.get_width()/2,330))
        help_controls=helpFont.render('Press C for controls',1, (255,100,250))
        display.blit(help_controls, (440,460))
        quitthis=helpFont.render('Press ESC to quit',1, (255,100,250))
        display.blit(quitthis, (0,460))
        pygame.display.update()
        ismenu=False

def gameoverscn():
    global pause,enemies,FPS,gun_ammo,missiles,score,ene_killed,T1Missile_Reserve,T1Ammunition,frame_count,S_time,isboss,bossene,ang,win,rev,ShotOnce
    rev=True
    win=0
    ShotOnce=False
    pause=0
    enemies=[]
    bossene=[]
    FPS=30
    gun_ammo=[]
    missiles=[]
    run=True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.set_volume(.6)
                run=False
        display.blit(Nightime, (0,0))
        pScoreFont=pygame.font.SysFont('tahoma',50)
        TIME=pScoreFont.render('Time survived :' + str(S_time),1, (255,230,85))
        display.blit(TIME, (screenwidth/2 - TIME.get_width()/2,50))
        Kills=pScoreFont.render('Enemies Killed :' + str(ene_killed),1, (255,0,0))
        display.blit(Kills, (screenwidth/2 - Kills.get_width()/2,100))
        Prev_Score=pScoreFont.render('High Score :' + str(updateScore()),1, (255,180,230))
        display.blit(Prev_Score, (screenwidth/2 - Prev_Score.get_width()/2,200))
        New_Score=pScoreFont.render('Score :' + str(score),1, (0,255,0))
        display.blit(New_Score, (screenwidth/2 - New_Score.get_width()/2,300))
        try_again=pScoreFont.render("Press LMB to try again",1, (255,255,255))
        display.blit(try_again, (screenwidth/2 - try_again.get_width()/2,390))
        pygame.display.update()
    jet.health=900
    jet.x=60
    jet.y=240
    jet.visible=True
    T1Missile_Reserve=10
    T1Ammunition=2000
    score=0    
    ene_killed=0
    frame_count=0
    isboss=False
    pygame.time.set_timer(pygame.USEREVENT+4,3000)
    pygame.time.set_timer(pygame.USEREVENT+5,3000)
    musicReload()
    
def endscn():
    global pause,enemies,FPS,gun_ammo,missiles,score,ene_killed,T1Missile_Reserve,T1Ammunition,frame_count,S_time,isboss,bossene,win,rev,ShotOnce,ang
    rev=True
    ShotOnce=False
    ang=0
    pause=0
    win=0
    enemies=[]
    bossene=[]
    FPS=30
    gun_ammo=[]
    missiles=[]
    run=True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.set_volume(.6)
                run=False
        keys=pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        display.blit(Nightime, (0,0))
        endFont=pygame.font.SysFont('system',40)
        str1=endFont.render('You did it!, the gruesome alien warship that',1, (255,255,255))
        display.blit(str1, (screenwidth/2 - str1.get_width()/2,50))
        str2=endFont.render('masterminded this invasion is blasted into',1, (255,255,255))
        display.blit(str2, (screenwidth/2 - str2.get_width()/2,85))
        obl=endFont.render('oblivion.',1, (255,255,255))
        display.blit(obl, (screenwidth/2 - obl.get_width()/2,115))
        str3=endFont.render('Your victory has enabled humankind to drive',1, (255,255,255))
        display.blit(str3, (screenwidth/2 - str3.get_width()/2,150))
        str4=endFont.render('out the last remaining alien forces.',1, (255,255,255))
        display.blit(str4, (screenwidth/2 - str4.get_width()/2,180))
        str5=endFont.render('Now that you saved Earth, you head back',1, (255,255,255))
        display.blit(str5, (screenwidth/2 - str5.get_width()/2,210))
        str6=endFont.render('to the capital, where you are hailed as hero.',1, (255,255,255))
        display.blit(str6, (screenwidth/2 - str6.get_width()/2,240))
        try_again=endFont.render("Press LMB to try again",1, (255,255,255))
        display.blit(try_again, (screenwidth/2 - try_again.get_width()/2,390))
        quit_game=endFont.render("Press ESC to quit",1, (255,255,255))
        display.blit(quit_game, (screenwidth/2 - quit_game.get_width()/2,420))
        pygame.display.update()
    jet.health=900
    jet.x=60
    jet.y=240
    jet.visible=True
    T1Missile_Reserve=10
    T1Ammunition=2000
    score=0    
    ene_killed=0
    frame_count=0
    isboss=False
    pygame.time.set_timer(pygame.USEREVENT+4,3000)
    pygame.time.set_timer(pygame.USEREVENT+5,3000)
    musicReload()
    
#Setup

pygame.init()
display=pygame.display.set_mode((screenwidth, screenheight))
icon=pygame.image.load('BS.ico')
pygame.display.set_caption('BattleSkies')
pygame.display.set_icon(icon)
clock=pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT+1,random.randrange(2000,3000))
pygame.time.set_timer(pygame.USEREVENT+2,random.randrange(1000,3000))
pygame.time.set_timer(pygame.USEREVENT+3,random.randrange(1000,5000))
pygame.time.set_timer(pygame.USEREVENT+4,3000)
pygame.time.set_timer(pygame.USEREVENT+5,3000)
backdropclouds=pygame.image.load('Textures/Clouds.png')
Daytime=pygame.image.load('Textures/Day.png')
Nightime=pygame.image.load('Textures/Night.png')
backdropbox=display.get_rect()
backdropclouds_size=backdropclouds.get_size()

Afterburners=[pygame.image.load('Textures/Reaper/Reaper6.png'),pygame.image.load('Textures/Reaper/Reaper7.png'),pygame.image.load('Textures/Reaper/Reaper8.png'),pygame.image.load('Textures/Reaper/Reaper9.png'),pygame.image.load('Textures/Reaper/Reaper10.png'),pygame.image.load('Textures/Reaper/Reaper11.png')]
Airbrakes=[pygame.image.load('Textures/Reaper/Reaper18.png'),pygame.image.load('Textures/Reaper/Reaper19.png'),pygame.image.load('Textures/Reaper/Reaper20.png'),pygame.image.load('Textures/Reaper/Reaper21.png'),pygame.image.load('Textures/Reaper/Reaper22.png'),pygame.image.load('Textures/Reaper/Reaper23.png')]
Ascent=[pygame.image.load('Textures/Reaper/Reaper12.png'),pygame.image.load('Textures/Reaper/Reaper13.png'),pygame.image.load('Textures/Reaper/Reaper14.png'),pygame.image.load('Textures/Reaper/Reaper15.png'),pygame.image.load('Textures/Reaper/Reaper16.png'),pygame.image.load('Textures/Reaper/Reaper17.png')]
Descent=[pygame.image.load('Textures/Reaper/Reaper24.png'),pygame.image.load('Textures/Reaper/Reaper25.png'),pygame.image.load('Textures/Reaper/Reaper26.png'),pygame.image.load('Textures/Reaper/Reaper27.png'),pygame.image.load('Textures/Reaper/Reaper28.png'),pygame.image.load('Textures/Reaper/Reaper29.png')]
JetNormal=[pygame.image.load('Textures/Reaper/Reaper0.png'),pygame.image.load('Textures/Reaper/Reaper1.png'),pygame.image.load('Textures/Reaper/Reaper2.png'),pygame.image.load('Textures/Reaper/Reaper3.png'),pygame.image.load('Textures/Reaper/Reaper4.png'),pygame.image.load('Textures/Reaper/Reaper5.png')]
Mugshot=[pygame.image.load('Textures/Mugshot/Mugshot100.png'),pygame.image.load('Textures/Mugshot/Mugshot80.png'),pygame.image.load('Textures/Mugshot/Mugshot50.png'),pygame.image.load('Textures/Mugshot/Mugshot30.png'),pygame.image.load('Textures/Mugshot/Mugshot10.png'),pygame.image.load('Textures/Mugshot/MugshotStatic1.png'),pygame.image.load('Textures/Mugshot/MugshotStatic2.png'),pygame.image.load('Textures/Mugshot/MugshotStatic3.png')]
HUD=pygame.image.load('Textures/HUD.png')

T1missile=pygame.image.load('Textures/MissileTier 1.png')
T1bullet=pygame.image.load('Textures/Bullet Tier1.png')
MaxAm=pygame.image.load('Textures/Max Ammo.png')
MaxHeal=pygame.image.load('Textures/Max Health.png')

BRRT=pygame.mixer.Sound('sound/MachineGun4.wav')
KaBoom=pygame.mixer.Sound('sound/Explosion3.wav')
MissileLaunch=pygame.mixer.Sound('sound/Missile2.wav')
Hitmarker=pygame.mixer.Sound('sound/ArrowHit1.wav')
BGM=pygame.mixer.music.load('music/BattleSkies Theme.mp3')

# BGBoss=pygame.mixer.music.load('music/Boss.mp3')
BRRT.set_volume(.09)
KaBoom.set_volume(.04)
MissileLaunch.set_volume(.3)
Hitmarker.set_volume(.05)

pygame.mixer.music.set_volume(.8)
BGCX=0
BGCX2=backdropclouds.get_width()

#Main Game Loop
ScoreFont=pygame.font.SysFont('tahoma',20)
killcount=pygame.font.SysFont('tahoma',15,1)
RocketCount=pygame.font.SysFont('quartz',25)
GameOver=pygame.font.SysFont('tahoma',50)
HealthPercentFont=pygame.font.SysFont('lcd',10,1)
jet=Reaper(60,240,64,64)
enemies=[]
shootPause=0
die=0
frame_count=0
powerUps=[]
gun_ammo=[]
missiles=[]

bossene=[]
pygame.mixer.music.play(-1)
while True: 
    if ismenu:
        pygame.mixer.music.set_volume(0)
        menu()
    
    t_seconds=frame_count//FPS
    minutes=t_seconds//60
    seconds=t_seconds%60
    frame_count+=1
    
    if pause>0:
        pause+=1
        if pause>die*2:
            gameoverscn()

    if win>0:
        win+=1
        if win>die*2:
            endscn()
            
    for enemy in enemies:
        enemy.move_bullets(jet.hitbox)
        if random.randrange(0, 30)==1:
            enemy.shoot()
        for rounds in gun_ammo:
            if rounds.hitmark(enemy.hitbox):
                enemy.hit(50)
                if enemy.visible:
                    score+=1
                    gun_ammo.pop(gun_ammo.index(rounds))
                else:  
                    KaBoom.play()
                    enemies.pop(enemies.index(enemy))
                    
        
        for missile in missiles:
            if missile.hitmark(enemy.hitbox):
                enemy.hit(1000)
                if enemy.visible:
                   score+=1
                   missiles.pop(missiles.index(missile)) 
                else:  
                    KaBoom.play()
                    enemies.pop(enemies.index(enemy))
                    
        
        if enemy.collide(jet.hitbox):
            jet.hit(100)
            if not jet.visible:
                if pause==0:
                    die=FPS
                    pause = 1
                    pygame.mixer.music.set_volume(0)
        
        if enemy.x < enemy.width * -10:
            enemies.pop(enemies.index(enemy))
                
    for powerUp in powerUps:
        if powerUp.collide(jet.hitbox):
            powerUp.hit()
            if powerUp.visible:
                powerUp.visible=False
            else:
                powerUps.pop(powerUps.index(powerUp))
    
    for bosss in bossene:
        percent=(bosss.health/5000)*100
        bosss.move_bullets(jet.hitbox)
        if percent>=80:
            patte()
        elif percent>=40 and percent<80:
            pattm()
            if not ShotOnce:
                bosss.shootM()
                powerUps.append(MaxHealth(random.randint(screenwidth+10,screenwidth+20),random.randint(100,screenheight-100),32))
                powerUps.append(MaxAmmo(random.randint(screenwidth+10,screenwidth+20),random.randint(100,screenheight-200),32))
                ShotOnce=True
                ang=0
                
        elif percent>=20 and percent<40:
            patth()
        
        elif percent>0 and percent<20:
            pattd()
        
        for rounds in gun_ammo:
            if rounds.hitmark(bosss.hitbox):
                bosss.hit(5)
                if bosss.visible:
                    score+=1
                    gun_ammo.pop(gun_ammo.index(rounds))
                else:  
                    KaBoom.play()
                    bosss.visible=False
                    bossene.pop(bossene.index(bosss))
                    if win==0:
                        die=FPS
                        win=1
                        pygame.mixer.music.set_volume(0)
                        
        for missile in missiles:
            if missile.hitmark(bosss.hitbox):
                bosss.hit(100)
                if bosss.visible:
                   score+=1
                   missiles.pop(missiles.index(missile)) 
                else:  
                    KaBoom.play()
                    bosss.visible=False
                    bossene.pop(bossene.index(bosss))
                    if win==0:
                        die=FPS
                        win=1
                        pygame.mixer.music.set_volume(0)
                        
        if bosss.collide(jet.hitbox):
                jet.hit(800)
                if not jet.visible:
                    if pause==0:
                        die=FPS
                        pause = 1
                        pygame.mixer.music.set_volume(0)
                    
    BGCX-=10.0
    BGCX2-=10.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.USEREVENT + 1:
            if not isboss:
                r=random.randrange(0,101)
                c=(r/100)*100
                if c <= 60:
                    enemies.append(Weak_Enemy(random.randint(screenwidth+10,screenwidth+20),random.randint(50,screenheight-80),64,64))
                if c > 60 and c <= 80:
                    enemies.append(Normal_Enemy(random.randint(screenwidth+10,screenwidth+20),random.randint(50,screenheight-80),64,64)) 
                if c > 80 and c <= 100:
                    enemies.append(Big_Enemy(random.randint(screenwidth+10,screenwidth+20),random.randint(50,screenheight-80),64,64))
        if event.type == pygame.USEREVENT + 2:
            if minutes%5==0 and minutes!=0 and seconds==0 and len(powerUps)==0:
                powerUps.append(MaxAmmo(random.randint(screenwidth+10,screenwidth+20),random.randint(100,screenheight-200),32))
            if minutes%10==0 and minutes!=0 and seconds==0 and len(powerUps)==0:
                powerUps.append(MaxHealth(random.randint(screenwidth+10,screenwidth+20),random.randint(100,screenheight-100),32))
    if (minutes==20 and seconds==0 and len(bossene)==0) or (ene_killed==100 and len(bossene)==0):
            bossene.append(Boss(random.randint(screenwidth+10,screenwidth+20),200,64,64,jet.x,jet.y))
            isboss=True
            pygame.mixer.music.stop()
            bossevent()
           
            
    if shootPause>0:
        shootPause+=1
    if shootPause>3:
        shootPause=0
    if BGCX < backdropclouds.get_width() * -1:  
        BGCX = backdropclouds.get_width()
            
    if BGCX2 < backdropclouds.get_width() * -1:
        BGCX2 = backdropclouds.get_width()
          
    if jet.visible:
        for rounds in gun_ammo:
            if rounds.x < screenwidth and rounds.x > 0:
                rounds.x+=rounds.steps
            
            else:
                gun_ammo.pop(gun_ammo.index(rounds))
    
        for missile in missiles:
            if missile.x < screenwidth and missile.x > 0:
                missile.x+=missile.steps
            else:
                missiles.pop(missiles.index(missile))
        
        keys=pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            quitgame()
        
        if keys[pygame.K_SPACE] and T1Ammunition>0 and shootPause==0 :
            if len(gun_ammo)<60:
                gun_ammo.append(_25(round(jet.x + jet.width//2),round(jet.y + jet.height//2),2))
                BRRT.play()
                T1Ammunition-=1
                shootPause=1
        if keys[pygame.K_m] and T1Missile_Reserve>0 and shootPause==0:
            if len(missiles)<1:
                missiles.append(Missile(round(jet.x + jet.width//2),round(jet.y + jet.height//2),2))
                MissileLaunch.play()
                T1Missile_Reserve-=1

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and jet.x > jet.steps:
            jet.x -=jet.steps
            jet.left=True
            jet.right=False
            jet.up=False
            jet.down=False
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and jet.x < screenwidth - jet.width - jet.steps:
            jet.x +=jet.steps
            jet.left=False
            jet.right=True
            jet.up=False
            jet.down=False
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and jet.y > jet.steps:
            jet.y-=jet.steps
            jet.left=False
            jet.right=False
            jet.up=True
            jet.down=False
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and jet.y < screenheight - jet.height - jet.steps:
            jet.y+=jet.steps
            jet.left=False
            jet.right=False
            jet.up=False
            jet.down=True
        else:
            jet.left=False
            jet.right=False
            jet.up=False
            jet.down=False
    
    DrawAnim(minutes,seconds)
    clock.tick(FPS)