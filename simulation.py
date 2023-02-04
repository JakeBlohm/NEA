import PySimpleGUI as sg
import random, sys, time, threading, statistics
import pygame as pg
import threading
from pygame.locals import (
    K_ESCAPE
)
from functions import SpriteRender, graphs, dataConverter,stringToRgb
from settings import SCREEN_HEIGHT,SCREEN_WIDTH,SCALE,screen
from sprites import simButtons
SIZE_SCALE = SCALE
class AnimalGroup(pg.sprite.Group):
    def update(self,foods,stats = None, index = ""):
        animals = self.sprites()
        if (index != ""):
            temp = []
            tempStats = [[],[],[],[],[]]
            for animal in animals:
                temp = animal.update(foods)
                for i in range(len(temp)):
                    tempStats[i].append(temp[i])

            if range(len(temp)) == 0:
                tempStats ={0,0,0,0,0}
            # self.speed, self.sight, self.fov, self.food, self.size
            statsDic ={}
            statsDic["Speed"] = statistics.mean(tempStats[0])
            statsDic["Sight"] = statistics.mean(tempStats[1])
            statsDic["FOV"] = statistics.mean(tempStats[2])
            statsDic["Food"] = statistics.mean(tempStats[3])
            statsDic["Size"] = statistics.mean(tempStats[4])
            stats[index] = statsDic
        else:
            for animal in animals:
                animal.update(foods)
        

class Animal(pg.sprite.Sprite):
    def __init__(self, group,screen, pos, stats, enviroConditions):
       # Call the parent class (Sprite) constructor
       pg.sprite.Sprite.__init__(self)

       # unpack data from stats
       # traits
       self.speed = self.evolve(stats["Speed"],stats["SpeedEM"],0)
       self.agility = self.evolve(stats["Agility"],stats["AgilityEM"],0)
       self.sight = self.evolve(stats["Sight"],stats["SightEM"],0)
       self.fov = self.evolve(stats["FOV"],stats["FOVEM"],0)
       self.size = self.evolve(stats["Size"],stats["SizeEM"],10)
       
       self.stats ={
    "Speed": self.speed,
    "SpeedEM": stats["SpeedEM"],
    "Agility": self.agility,
    "AgilityEM": stats["AgilityEM"],
    "Size": self.size,
    "SizeEM": stats["SizeEM"],
    "Sight": self.sight,
    "SightEM": stats["SightEM"],
    "FOV": self.fov,
    "FOVEM": stats["FOVEM"],
    "Eats Berrys": False
    }
       self.enviroConditions = enviroConditions

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       spriteSize = (self.size/10)*SIZE_SCALE
       self.image = pg.Surface([spriteSize, spriteSize])
       if self.speed*20 < 255:
        self.image.fill((0,0,self.speed*20))
       else:
        self.image.fill((0,0,255))

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect(center = pos)
       self.radius = spriteSize/2

       self.group = group
       group.add(self)
       
       self.cycle = 0
       self.foundTarget = False
       # sets the spawn bearing to a random number
       bearing = random.randint(0,360)
       self.vector = pg.math.Vector2(1,0).rotate(bearing)
       self.screen = screen
       

       self.foodDrain = (self.speed*enviroConditions[0])+(self.agility*enviroConditions[1])+(self.sight*enviroConditions[2])+(self.fov*enviroConditions[3])

       # stats
       self.food = self.size/2
       self.health = self.size
       self.pos = pos

    def evolve(self,trait,traitMod,traitMin=1):
        trait += random.uniform(-traitMod,traitMod)
        if trait < traitMin:
            trait = traitMin
        return trait
    
    def createChild(self):
        Animal(self.group,self.screen, self.pos,self.stats,self.enviroConditions)

    def lookFor(self, targets):
        self.foundTarget = False
        self.targetDistance = 0

        viewDis = self.sight*SCALE
        position = self.rect.center

        high = [position[0] + viewDis, position[1] + viewDis]
        low = [position[0] - viewDis, position[1] - viewDis]

        for target in targets:
            targetPos = target.rect.center
            if low[0] < targetPos[0] < high[0] and low[1] < targetPos[1] < high[1]:
                targetVector = pg.math.Vector2(targetPos[0] - position[0],targetPos[1] - position[1])
                distance = targetVector.magnitude()
                angle = self.vector.angle_to(targetVector)
                if -self.fov < angle < self.fov and viewDis > distance:
                    if self.foundTarget == False or self.targetDistance > distance:
                        self.targetDistance = distance
                        self.targetAngle = angle
                        self.foundTarget = True
                        self.target = target 
                        
    def locateTarget(self,target):
        self.foundTarget = False
        viewDis = self.sight*SCALE
        position = self.rect.center

        targetPos = target.rect.center
        targetVector = pg.math.Vector2(targetPos[0] - position[0],targetPos[1] - position[1])
        distance = targetVector.magnitude()
        angle = self.vector.angle_to(targetVector)
        if -self.fov < angle < self.fov and viewDis > distance:
            self.targetDistance = distance
            self.targetAngle = angle
            self.foundTarget = True

    def update(self, foods):
        self.food -= self.foodDrain
        self.cycle += 1

        if self.food <= 0:
            self.health -= 0.5
            self.food = 0

            if self.speed*20 < 255 and self.health > 0:
                self.image.fill((int(255-(255*(self.health/self.size))),0,int(self.speed)*20))
            else:
                self.health = 0
                self.image.fill((int(255-(255*(self.health/self.size))),0,255))
        elif self.food > self.size /4 and self.health < self.size:
            self.food -= 0.5
            self.health += 0.5
            if self.health > self.size:
                self.health = self.size

            if self.speed*20 < 255:
                self.image.fill((int(255-(255*(self.health/self.size))),0,int(self.speed)*20))
            else:
                self.image.fill((int(255-(255*(self.health/self.size))),0,255))

        if self.health <= 0:
            self.kill()
        
        if len(foods) != 0 :
            if self.foundTarget == True:
                if self.cycle % 5 == 0:
                    self.lookFor(foods)
                else:
                    self.locateTarget(self.target)
            elif self.cycle % 20 == 0:
                self.lookFor(foods)

            if self.foundTarget:
                # Target or eat the targeted food
                if self.targetDistance < self.radius + self.target.radius:
                    self.targetValue = self.target.eat()
                    if self.targetValue > 0:
                        self.food += self.targetValue
                    self.foundTarget = False
                if self.targetAngle < 0:
                    if abs(self.targetAngle) > self.agility:
                        self.vector.rotate_ip(-self.agility)
                elif self.targetAngle > 0:
                    if abs(self.targetAngle) > self.agility:
                        self.vector.rotate_ip(self.agility)
            else:
                # Move randomly if there is no target
                self.vector.rotate_ip(random.uniform(-self.agility,self.agility))
        else:
            # Move randomly if there is no target
            self.vector.rotate_ip(random.uniform(-self.agility,self.agility))
        

        
        self.pos = (self.pos[0]+self.vector.x*self.speed,self.pos[1]+self.vector.y*self.speed)

        # Moves the sprite if it is off screen
        if self.rect.left < 0:
            self.pos = (SCREEN_WIDTH - self.image.get_width()/1.50,SCREEN_HEIGHT - self.pos[1])
            self.foundTarget = False
        elif self.rect.right > SCREEN_WIDTH:
            self.pos = (0 + self.image.get_width()/1.50,SCREEN_HEIGHT - self.pos[1])
            self.foundTarget = False
        if self.rect.top <= 0:
            self.pos = (SCREEN_WIDTH - self.pos[0],SCREEN_HEIGHT - self.image.get_height()/1.50)
            self.foundTarget = False
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.pos = (SCREEN_WIDTH - self.pos[0],0 + self.image.get_height()/1.50)
            self.foundTarget = False
        self.rect.center = self.pos
        
        # Tests if it has enouge food to reproduce
        if self.food > self.size * 1.5:
            self.createChild()
            self.food -= self.size
        
        # Draws lines showing where it is looking/targeting
        if self.foundTarget:
            pg.draw.line(self.screen,(255,0,0),self.rect.center,self.target.rect.center)
        else:
            pg.draw.line(self.screen,(0,125,0),self.rect.center,(self.vector.x*self.sight+self.pos[0],self.vector.y*self.sight+self.pos[1]))
            
        
        return [self.speed, self.sight, self.fov, self.food, self.size]


class FoodGroup(pg.sprite.Group):
    def __init__(self, amountOfFood, foodValue,foodPerCycle, *args, **kwargs):
        super(FoodGroup, self).__init__(*args, **kwargs)
        self.foodPerCycle = foodPerCycle
        self.amountOfFood = amountOfFood
        self.foodValue = foodValue
    amount = 0
    def update(self):
        self.amount += self.foodPerCycle
        if self.amount > self.amountOfFood:
            self.amount = self.amountOfFood
        while len(self.sprites()) < self.amountOfFood and self.amount >= 1:
            self.amount -= 1
            Food(self,self.foodValue)


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


class Simulation:
    def __init__(self,screen,animals,enviroConditions):
        print("Seting Up")
        # General setup
        self.screen = screen
        amountOfFood = enviroConditions[0][0]
        foodValue = enviroConditions[0][1]
        foodPerCycle = enviroConditions[0][2]

        self.clock = pg.time.Clock()
        self.running = True
        # Group setup
        self.foods = FoodGroup(amountOfFood,foodValue,foodPerCycle)

        # Animal setup
        self.animals = []
        self.animalsNames = []
        self.animalColours = []
        for animal in animals:
            quantity = animal[0]
            animal = animal[1]
            animalGroup = AnimalGroup()
            self.animals.append(animalGroup)
            self.animalsNames.append(animal["Name"])
            self.animalColours.append(stringToRgb(animal["Name"]))
            for i in range(0,quantity):
                Animal(animalGroup,self.screen, (random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT)),animal,enviroConditions[1])

        for i in range(0,amountOfFood):
            Food(self.foods,foodValue)

        print("Set Up")
        self.animalsData = {}
        self.cycles = 0
        self.graphView = False
        self.dataTypes = ["Speed", "Sight", "FOV", "Food", "Size"]

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

        while self.running:
            mClick = False
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                elif event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    mClick = True
            self.screen.fill((50,150,50))
            self.foods.draw(self.screen)
            self.foods.update()

            s = time.perf_counter()
            threads = []
            if (self.cycles % 100 == 0):
                stats = {}
                for name in self.animalsNames:
                    stats[name] = None
                for i  in range(len(self.animals)):
                    threads.append(threading.Thread(target = self.animals[i].update, args=(self.foods,stats,self.animalsNames[i],)))
            else:
                for animal in self.animals:
                    threads.append(threading.Thread(target = animal.update, args=(self.foods,)))

            for thread in threads:
                thread.start()
            
            for thread in threads:
                thread.join()

            if (self.cycles % 100 == 0):
                print(stats)
                self.animalsData[self.cycles] = stats
                if (self.cycles > 100) and self.graphView:
                    self.newData,self.dataScales = dataConverter(self.animalsData,self.dataTypes,self.animalsNames)

            f = time.perf_counter()
            #print(f"it took {f - s}s")


            for animal in self.animals:
                animal.draw(self.screen)

            mousePos=pg.mouse.get_pos()
            if simButtons.update(mousePos,mClick)[0]!= None:
                self.graphView = not(self.graphView)
                print(self.animalsData)
                self.newData,self.dataScales = dataConverter(self.animalsData,self.dataTypes,self.animalsNames)

            if self.graphView:
                SpriteRender((400,900),(100,100,100,10),(1400,450),self.screen)
                if (self.cycles > 200):
                    for animalNum in range(len(self.animals)):
                        for i in range(5):
                            graphs(self.newData,self.dataScales,animalNum,self.dataTypes[i],(1420,160*i + 150),(1.7,0.6),self.animalColours[animalNum])
                
            
            simButtons.draw(self.screen)

            self.displayFps()

            self.clock.tick()


            self.cycles += 1
            pg.display.flip()
        return self.animalsData
#sim = Simulation(screen,[[10, {'Speed': 10, 'SpeedEM': 1, 'Agility': 10, 'AgilityEM': 1, 'Size': 1000, 'SizeEM': 10, 'Sight': 100, 'SightEM': 10, 'FOV': 45, 'FOVEM': 20, 'Eats Berrys': False, 'Name': 'Big'}], [100, {'Speed': 10, 'SpeedEM': 1, 'Agility': 10, 'AgilityEM': 1, 'Size': 100, 'SizeEM': 10, 'Sight': 100, 'SightEM': 10, 'FOV': 45, 'FOVEM': 20, 'Eats Berrys': False, 'Name': 'Default'}]],[[100,50,20],[0.01,0.01,0.001,0.001]])
#sim.run()