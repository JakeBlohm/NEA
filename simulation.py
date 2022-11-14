from copy import copy
import PySimpleGUI as sg
from numpy import average
import random, sys, time, math, pyautogui, threading, platform
import pygame as pg
from pygame.locals import (
    K_ESCAPE
)

OS = platform.system()

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
print(pyautogui.size())
if SCREEN_WIDTH >= SCREEN_HEIGHT:
    SCALE = SCREEN_HEIGHT
else:
    SCALE = SCREEN_WIDTH

SIZE_SCALE = SCALE / 1000
SCALE /= 1000

speedMod = 1
rotSpeedMod = 1
viewDisMod = 10
viewAngleMod = 5
childCostMod = 100

foodPerCycle = 0.1
foodValue = 100

speedDrain = 0.01
rotSpeedDrain = 0.01
viewDisDrain = 0.001
viewAngleDrain = 0.005

startSpeed = 1
startRotSpeed = 1
startViewDis = 100
startViewAngle = 45

startingFood = 100
startingHealth = 100

childCost = 100
amountOfFood = 100
amountOfAnimals = 1000
TITLE = 'Evolution'



class AnimalGroup(pg.sprite.Group):
    def update(self,foods):
        Speeds = []
        pop = 0
        veiwDiss = []
        veiwAngles = []
        foodAmount = []
        childCosts = []
        animals = self.sprites()
        for animal in animals:
            traits = animal.move(foods)
            Speeds.append(traits[0])
            veiwDiss.append(traits[1])
            veiwAngles.append(traits[2])
            foodAmount.append(traits[3])
            childCosts.append(traits[4])
            pop += 1
        return Speeds, pop, veiwDiss ,veiwAngles, foodAmount, childCosts

class Animal(pg.sprite.Sprite):
    def __init__(self, group,screen, pos, speed, rotSpeed, viewDis, viewAngle, childCost):
       # Call the parent class (Sprite) constructor
       pg.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.size = childCost/10
       self.image = pg.Surface([self.size*SIZE_SCALE, self.size*SIZE_SCALE])
       self.image.fill((0,0,speed*20))

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect(center = pos)
       self.radius = self.image.get_height()/2
       self.group = group
       group.add(self)
       
       self.cycle = 0
       self.foundTarget = False
       bearing = random.randint(0,360)
       self.vector = pg.math.Vector2(1,0).rotate(bearing)
       self.screen = screen
       # traits
       self.speed = self.evolve(speed,speedMod,0)
       self.rotSpeed = self.evolve(rotSpeed,rotSpeedMod,0)
       self.viewDis = self.evolve(viewDis,viewDisMod,0)
       self.viewAngle = self.evolve(viewAngle,viewAngleMod,0)
       self.childCost = self.evolve(childCost,childCostMod,10)

       self.foodDrain = (self.speed*speedDrain)+(self.rotSpeed*rotSpeedDrain)+(self.viewDis*viewDisDrain)+(self.viewAngle*viewAngleDrain)

       # stats
       self.food = childCost/2
       self.health = startingHealth
       self.pos = pos

    def evolve(self,trait,traitMod,traitMin=1):
        trait += random.randint(-traitMod,traitMod)
        if trait < traitMin:
            trait = traitMin
        return trait
    
    def createChild(self):
        Animal(self.group,self.screen, self.pos, self.speed, self.rotSpeed, self.viewDis, self.viewAngle, self.childCost)

    def lookFor(self, targets):
        self.foundTarget = False
        self.targetDistance = 0
        
        viewDis = self.viewDis*SCALE
        position = self.rect.center

        high = [position[0] + viewDis, position[1] + viewDis]
        low = [position[0] - viewDis, position[1] - viewDis]

        for target in targets:
            targetPos = target.rect.center
            if low[0] < targetPos[0] < high[0] and low[1] < targetPos[1] < high[1]:
                targetVector = pg.math.Vector2(targetPos[0] - position[0],targetPos[1] - position[1])
                distance = targetVector.magnitude()
                angle = self.vector.angle_to(targetVector)
                if -self.viewAngle < angle < self.viewAngle:
                    if self.foundTarget == False or self.targetDistance > distance:
                        self.targetDistance = distance
                        self.targetAngle = angle
                        self.foundTarget = True
                        self.target = target 

    def move(self, foods):
        self.food -= self.foodDrain
        self.cycle += 1
        if self.food < 0:
            self.kill()
        
        if self.foundTarget == True:
            self.lookFor(foods)
        elif self.cycle % 10 ==0:
            self.lookFor(foods)
        test = self.vector.xy
        if self.foundTarget:
            if self.targetDistance < self.radius + self.target.radius:
                self.targetValue = self.target.eat()
                if self.targetValue > 0:
                    self.food += self.targetValue
            if self.targetAngle < 0:
                if abs(self.targetAngle) > self.rotSpeed:
                    self.vector.rotate_ip(-self.rotSpeed)
            elif self.targetAngle > 0:
                if abs(self.targetAngle) > self.rotSpeed:
                    self.vector.rotate_ip(self.rotSpeed)
        else:
            self.vector.rotate_ip(random.randint(-self.rotSpeed,self.rotSpeed))
        
        
        self.pos = (self.pos[0]+self.vector.x*self.speed,self.pos[1]+self.vector.y*self.speed)

        if self.rect.left < 0:
            self.pos = (SCREEN_WIDTH - self.image.get_width()/1.50,SCREEN_HEIGHT - self.pos[1])
        if self.rect.right > SCREEN_WIDTH:
            self.pos = (0 + self.image.get_width()/1.50,SCREEN_HEIGHT - self.pos[1])
        if self.rect.top <= 0:
            self.pos = (SCREEN_WIDTH - self.pos[0],SCREEN_HEIGHT - self.image.get_height()/1.50)
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.pos = (SCREEN_WIDTH - self.pos[0],0 + self.image.get_height()/1.50)
        self.rect.center = self.pos
        
        if self.food > self.childCost * 1.5:
            self.createChild()
            self.food -= self.childCost

        if self.foundTarget:
            pg.draw.line(self.screen,(255,0,0),self.rect.center,self.target.rect.center)
        else:
            pg.draw.line(self.screen,(0,125,0),self.rect.center,(self.vector.x*self.viewDis+self.pos[0],self.vector.y*self.viewDis+self.pos[1]))
            

        return self.speed, self.viewDis, self.viewAngle, self.food, self.childCost
        #self.createChild()

class FoodGroup(pg.sprite.Group):
    amount = 0
    def update(self):
        self.amount += foodPerCycle
        if self.amount > amountOfFood:
            self.amount = amountOfFood
        while len(self.sprites()) < amountOfFood and self.amount >= 1:
            self.amount -= 1
            Food(self,foodValue)

class Food(pg.sprite.Sprite):
    def __init__(self,group,value):
       # Call the parent class (Sprite) constructor
       pg.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pg.Surface([5*SIZE_SCALE, 5*SIZE_SCALE])
       self.image.fill((150,200,255))
       self.radius = self.image.get_height()/2

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       pos = (random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT))
       for food in group.sprites():
           if food.pos == pos:
               pos = (random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT))
        
       self.pos = pos
       self.value = value

       self.rect = self.image.get_rect(center = pos)
       self.group = group
       group.add(self)
    def eat(self):
        self.kill()
        tempValue = self.value
        self.value = 0
        return tempValue

class Game:
    def __init__(self,animals):
        print("Seting Up")
        # General setup
        pg.init()
        self.screen = pg.display.set_mode((0,0),pg.FULLSCREEN, display=0)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        # Group setup
        self.foods = FoodGroup()

        # Animal setup
        for animal in animals:
            name = animal[0]
            amountOfAnimals = animal[1]
            stats = animal[2]
            animalGroup = AnimalGroup(name)
            self.animals.append(animalGroup)
            for i in range(0,amountOfAnimals):
                Animal(animalGroup,self.screen, (random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT)),stats)

        for i in range(0,amountOfFood):
            Food(self.foods,foodValue)
        print("Set Up")
        self.speeds = []
        self.pop = 0
        self.viewDiss = []
        self.viewAngles = []
        self.cycles = 0

    def render(self, font, data, color, pos):
        text = font.render(data, 0, pg.Color(color))
        self.screen.blit(text, pos)

    def displayFps(self):
        self.render(
            pg.font.SysFont('Arial', int(24*SCALE)),
            data=str(int(self.clock.get_fps())),
            color='white',
            pos=(0,0))

    def displayNum(self,position,num,colour):
        self.render(
            pg.font.SysFont('Arial', int(24*SCALE)),
            data=str(num),
            color=colour,
            pos=position)

    def run(self):
        # this is the run graph thing
        if OS == 'Windows':
            self.graphThread.start()
        else:
            print(OS)
        while self.running:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == K_ESCAPE:
                        pg.quit()
                        sys.exit()
                elif event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            self.screen.fill((50,150,50))
            self.foods.draw(self.screen)
            self.foods.update()
            self.speeds, self.pop, self.viewDiss, self.viewAngles, self.foodAmount, self.childCost = self.animals.update(self.foods)
            self.animals.draw(self.screen)
            self.displayFps()
            a= round(sum(self.foodAmount) / self.pop)
            b= round(sum(self.childCost) / self.pop)
            self.foodAmount.sort()
            c = round(self.foodAmount[0],1)
            self.displayNum((0*SCALE, 25*SCALE),self.pop,'white')
            self.displayNum((0*SCALE, 50*SCALE),a,'white')
            self.displayNum((50*SCALE, 50*SCALE),c,'white')
            self.displayNum((0*SCALE, 75*SCALE),b,'white')
            self.clock.tick()
            self.cycles += 1
            pg.display.flip()
            #time.sleep(0.05)

game = Game()
game.run()