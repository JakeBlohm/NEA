import sys
import time
import pyautogui
import os
import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
print(pyautogui.size())
SCALE =SCREEN_WIDTH

SCALE = SCALE/1600
print(SCALE)
FPS = 10

    # A group that can controll multiple buttions
class ButtonGroup(pg.sprite.Group):
    def update(self,mousePos):
        pressed = []
        buttions = self.sprites()
        for buttion in buttions:
            pressed.append(buttion.update(mousePos))
        return pressed
    def draw(self, screen):
        Buttions = self.sprites()
        for Buttion in Buttions:
            Buttion.draw(screen)
        
    def setText(self,data):
        Buttions = self.sprites()
        for Buttion in Buttions:
            Buttion.setText(data)

class Button(pg.sprite.Sprite):
    def __init__(self,size,textSize,screenText,name,colour, textColour,pos,group):
        print("Creating Buttion")
        # Create Buttion
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([size[0]*SCALE, size[1]*SCALE])
        self.image.fill(colour)
        self.rect = self.image.get_rect(center = (pos[0]*SCALE,pos[1]*SCALE))

        self.font = pg.font.SysFont('Arial', int(24*SCALE*textSize))
        self.text = self.font.render(screenText, 0, pg.Color(textColour))

        group = group
        group.add(self)

        self.name = name
        self.screenText = screenText
        self.textColour = textColour
        self.colour = colour
        self.highlight = False

    def update(self,mousePos):
        # detect if the mouse is on the buttion
        if self.rect.collidepoint(mousePos):
            # add highlight effect
            self.image.fill((self.colour[0]-50,self.colour[1]-50,self.colour[2]-50))
            self.highlight = True
            # detect when the mouse buttion is pressed
            if pg.mouse.get_pressed() == (True,False,False):
                return self.name

        elif self.highlight:
            # remove highlight effect
            self.image.fill(self.colour)
            self.highlight = False

    def draw(self,screen):
        # display the buttion then text
        screen.blit(self.image,self.rect)
        screen.blit(self.text,self.rect)
    
    def setText(self,data):
        if self.name in data:
            self.screenText = data[self.name]
            self.text = self.font.render(self.screenText, 0, pg.Color(self.textColour))

class BoxGroup(pg.sprite.Group):
    def update(self,mousePos):
        clicked = 0
        boxes = self.sprites()
        for box in boxes:
            clicked += box.update(mousePos)
        return clicked

    def draw(self, screen):
        boxes = self.sprites()
        for box in boxes:
            box.draw(screen)

    def getValues(self):
        dictionary = {}
        boxes = self.sprites()
        for box in boxes:
            name,value=(box.getValue())
            dictionary[name] = value
        return(dictionary)

    def setValues(self,data):
        boxes = self.sprites()
        for box in boxes:
            box.setValue(data)

class TextBox(pg.sprite.Sprite):
    def __init__(self,size,textSize,startValue,name,valueType,colour, textColour,pos,group,deleteValueOnClick = False):
        print("Creating TextBox")
        # Create TextBox
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([size[0]*SCALE, size[1]*SCALE])
        self.image.fill(colour)
        self.rect = self.image.get_rect(center = (pos[0]*SCALE,pos[1]*SCALE))
        
        self.value = startValue
        self.font = pg.font.SysFont('Arial', int(24*SCALE*textSize))
        self.text = self.font.render(startValue, 0, pg.Color(textColour))

        group = group
        group.add(self)

        self.valueType = valueType
        self.deleteValue = deleteValueOnClick
        self.name = name
        self.colour = colour
        self.textColour = textColour
        self.highlight = False
    
    def update(self,mousePos):
        # detect if the mouse is on the buttion
        if self.rect.collidepoint(mousePos):
            # add highlight effect
            self.image.fill((self.colour[0]-50,self.colour[1]-50,self.colour[2]-50))
            self.highlight = True
            # detect when the mouse buttion is pressed
            if pg.mouse.get_pressed() == (True,False,False):
                if self.valueType == "Number":
                    if self.deleteValue:
                        value = NumEditor()
                    else:
                        value = NumEditor(self.value)
                elif self.valueType == "Text":
                    if self.deleteValue:
                        value = TextEditor()
                    else:
                        value = TextEditor(self.value)
                if value != None:
                    self.value = value
                    self.text = self.font.render(value, 0, pg.Color(self.textColour))
                return 0.4

        elif self.highlight:
            # remove highlight effect
            self.image.fill(self.colour)
            self.highlight = False
        return 0

    def draw(self,screen):
        # display the buttion then text
        screen.blit(self.image,self.rect)
        screen.blit(self.text,self.rect)
    
    def getValue(self):
        return self.name,self.value
    
    def setValue(self,data):
        if self.name in data:
            self.value = data[self.name]
            self.text = self.font.render(self.value, 0, pg.Color(self.textColour))

class TickBox(pg.sprite.Sprite):
    def __init__(self,size,textSize,startValue,name,colour,textColour,pos,group):
        print("Creating TextBox")
        # Create TickBox
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([size[1]*SCALE, size[1]*SCALE])
        self.cutout = pg.Surface([size[1]*SCALE * 0.8, size[1]*SCALE * 0.8])
        self.image.fill(textColour)
        self.cutout.fill(colour)
        self.rect = self.image.get_rect(midright = (pos[0]*SCALE + size[0]*SCALE/2,pos[1]*SCALE))
        self.rectCutout = self.cutout.get_rect(midright = (pos[0]*SCALE + size[0]*SCALE/2 - size[1]*SCALE * 0.1,pos[1]*SCALE))
        self.font = pg.font.SysFont('Arial', int(24*SCALE*textSize))
        self.text = self.font.render(name, 0, pg.Color(textColour))

        group = group
        group.add(self)

        self.pos = (pos[0] * SCALE - (size[0]*SCALE)/2,pos[1] * SCALE - (size[1]*SCALE)/2)
        self.name = name
        self.textColour = textColour
        self.value = startValue
        self.highlight = False
    
    def update(self,mousePos):
        # detect if the mouse is on the buttion
        if self.rect.collidepoint(mousePos):
            # add highlight effect
            self.image.fill((self.textColour[0]-50,self.textColour[1]-50,self.textColour[2]-50))
            self.highlight = True
            # detect when the mouse buttion is pressed
            if pg.mouse.get_pressed() == (True,False,False):
                self.value = not self.value
                return 0.3

        elif self.highlight:
            # remove highlight effect
            self.image.fill(self.textColour)
            self.highlight = False
        return 0

    def draw(self,screen):
        # display the buttion then text
        screen.blit(self.image,self.rect)
        if self.value:
            screen.blit(self.cutout,self.rectCutout)
        screen.blit(self.text,self.pos)
    
    def getValue(self):
        return self.name,self.value
    
    def setValue(self,data):
        if self.name in data:
            self.value = data[self.name]

class DefaultGroup(pg.sprite.Group):
    def draw(self,screen):
        sprites = self.sprites()
        for sprite in sprites:
            sprite.draw(screen)
    def setText(self,data):
        sprites = self.sprites()
        for sprite in sprites:
            sprite.setText(data)

class Text(pg.sprite.Sprite):
    def __init__(self,textSize,text,textColour,pos,group,size = None,colour = None, alignment = "center", name = None):
        print("Creating Text")
        # Create Buttion
        pg.sprite.Sprite.__init__(self)
        if size != None:
            self.image = pg.Surface([size[0]*SCALE, size[1]*SCALE])
            self.image.fill(colour)
            self.rect = self.image.get_rect(center = (pos[0]*SCALE,pos[1]*SCALE))

            font = pg.font.SysFont('Arial', int(24*SCALE*textSize))
            self.text = font.render(text, 0, pg.Color(textColour))
            self.backround = True
        else:
            font = pg.font.SysFont('Arial', int(24*SCALE*textSize))
            self.text = font.render(text, 0, pg.Color(textColour))
            if alignment == "center":
                self.rect = self.text.get_rect(center = (pos[0]*SCALE,pos[1]*SCALE))
            elif alignment == "left":
                self.rect = self.text.get_rect(midleft = (pos[0]*SCALE,pos[1]*SCALE))
            elif alignment == "right":
                self.rect = self.text.get_rect(midright = (pos[0]*SCALE,pos[1]*SCALE))
            self.backround = False

        self.name = name
        self.font = font
        self.textColour = textColour
        group = group
        group.add(self)

    def draw(self,screen):
        # display the buttion then text
        if self.backround:
            screen.blit(self.image,self.rect)
        screen.blit(self.text,self.rect)
    
    def setText(self,data):
        if self.name in data:
            text = data[self.name]
            self.text = self.font.render(text, 0, pg.Color(self.textColour))
    
def TextRender(text,scale,colour,pos,screen):
    font = pg.font.SysFont('Arial', int(24*SCALE*scale))
    text = font.render(text, 0, pg.Color(colour))
    rect = text.get_rect(center = (pos[0]*SCALE,pos[1]*SCALE))
    screen.blit(text,rect)

def SpriteRender(size,colour,pos,screen):
    image = pg.Surface([size[0]*SCALE, size[1]*SCALE])
    image.fill(colour)
    rect = image.get_rect(center = (pos[0]*SCALE,pos[1]*SCALE))
    screen.blit(image,rect)


def setup():
    # Make all the parts for the Menu
    menuButtons = ButtonGroup()
    Button((460,50),2,"Creature Creator","Creature Creator",(255,255,255),(0,0,0),(250,50),menuButtons)
    Button((460,50),2,"Environment Creator","Environment Creator",(255,255,255),(0,0,0),(250,125),menuButtons)
    Button((460,50),2,"Setup/Run Simulation","Simulation Creator",(255,255,255),(0,0,0),(250,200),menuButtons)

    creatureCreatorButtons = ButtonGroup()
    Button((100,50),2,"Exit","Exit",(255,255,255),(0,0,0),(75,850),creatureCreatorButtons)
    Button((125,50),2,"Save","Save",(255,255,255),(0,0,0),(1500,850),creatureCreatorButtons)
    Button((125,50),2,"Load","Load",(255,255,255),(0,0,0),(1350,850),creatureCreatorButtons)
    Button((150,50),2,"Delete","Delete",(255,255,255),(0,0,0),(1175,850),creatureCreatorButtons)
    creatureCreatorBox = BoxGroup()
    TextBox((300,25),1,"Name","Name","Text",(255,255,255),(0,0,0),(1400,50),creatureCreatorBox,True)
    TextBox((200,25),1,"1","Speed","Number",(255,255,255),(0,0,0),(300,50),creatureCreatorBox,True)
    TextBox((200,25),1,"1","SpeedEM","Number",(255,255,255),(0,0,0),(550,50),creatureCreatorBox,True)
    TextBox((200,25),1,"1","SpeedFD","Number",(255,255,255),(0,0,0),(800,50),creatureCreatorBox,True)
    TextBox((200,25),1,"1","Health","Number",(255,255,255),(0,0,0),(300,100),creatureCreatorBox,True)
    TextBox((200,25),1,"1","HealthEM","Number",(255,255,255),(0,0,0),(550,100),creatureCreatorBox,True)
    TextBox((200,25),1,"1","HealthFD","Number",(255,255,255),(0,0,0),(800,100),creatureCreatorBox,True)
    TextBox((200,25),1,"1","VisionDistance","Number",(255,255,255),(0,0,0),(300,150),creatureCreatorBox,True)
    TextBox((200,25),1,"1","VisionDistanceEM","Number",(255,255,255),(0,0,0),(550,150),creatureCreatorBox,True)
    TextBox((200,25),1,"1","VisionDistanceFD","Number",(255,255,255),(0,0,0),(800,150),creatureCreatorBox,True)
    TextBox((200,25),1,"45","FOV","Number",(255,255,255),(0,0,0),(300,200),creatureCreatorBox,True)
    TextBox((200,25),1,"1","FOVEM","Number",(255,255,255),(0,0,0),(550,200),creatureCreatorBox,True)
    TextBox((200,25),1,"1","FOVFD","Number",(255,255,255),(0,0,0),(800,200),creatureCreatorBox,True)
    TickBox((200,25),1,False,"Eats Berrys",(0,0,0),(255,255,255),(300,250),creatureCreatorBox)
    creatureCreatorDefault = DefaultGroup()
    Text(1,"Name",(255,255,255),(1400,25),creatureCreatorDefault)
    Text(1,"Base Value",(255,255,255),(300,25),creatureCreatorDefault)
    Text(1,"Evolution Modifier",(255,255,255),(550,25),creatureCreatorDefault)
    Text(1,"Food Drain",(255,255,255),(800,25),creatureCreatorDefault)
    Text(1,"Speed",(255,255,255),(0,50),creatureCreatorDefault,alignment="left")
    Text(1,"Health",(255,255,255),(0,100),creatureCreatorDefault,alignment="left")
    Text(1,"VisionDistance",(255,255,255),(0,150),creatureCreatorDefault,alignment="left")
    Text(1,"FOV",(255,255,255),(0,200),creatureCreatorDefault,alignment="left")

    environmentCreatorButtons = ButtonGroup()
    Button((100,50),2,"Exit","Exit",(255,255,255),(0,0,0),(75,850),environmentCreatorButtons)
    Button((125,50),2,"Save","Save",(255,255,255),(0,0,0),(1500,850),environmentCreatorButtons)
    Button((125,50),2,"Load","Load",(255,255,255),(0,0,0),(1350,850),environmentCreatorButtons)
    environmentCreatorBox = BoxGroup()
    TextBox((300,25),1,"Name","Name","Text",(255,255,255),(0,0,0),(1400,50),environmentCreatorBox,True)
    environmentCreatorDefault = DefaultGroup()
    Text(1,"Name",(255,255,255),(1400,25),environmentCreatorDefault)
    Text(1,"Creatures",(255,255,255),(75,25),environmentCreatorDefault)

    simulationCreatorButtons = ButtonGroup()
    Button((100,50),2,"Exit","Exit",(255,255,255),(0,0,0),(75,850),simulationCreatorButtons)
    Button((125,50),2,"Save","Save",(255,255,255),(0,0,0),(1500,850),simulationCreatorButtons)
    Button((125,50),2,"Load","Load",(255,255,255),(0,0,0),(1350,850),simulationCreatorButtons)
    Button((350,50),2,"Select Creature","Select Creature",(255,255,255),(0,0,0),(200,750),simulationCreatorButtons)
    
    simulationCreatorBox = BoxGroup()
    TextBox((300,25),1,"Name","Name","Text",(255,255,255),(0,0,0),(1400,50),simulationCreatorBox,True)
    simulationCreatorDefault = DefaultGroup()
    Text(1,"Name",(255,255,255),(1400,25),simulationCreatorDefault)
    Text(1,"Creatures",(255,255,255),(75,25),simulationCreatorDefault)

    textEditorButtons = ButtonGroup()
    Button((100,25),1,"Cancel","Cancel",(255,255,255),(0,0,0),(700,500),textEditorButtons)
    Button((100,25),1,"Confirm","Confirm",(255,255,255),(0,0,0),(900,500),textEditorButtons)

    confirmButtons = ButtonGroup()
    Button((100,25),1,"Cancel","Cancel",(255,255,255),(0,0,0),(700,500),confirmButtons)
    Button((100,25),1,"Confirm","Confirm",(255,255,255),(0,0,0),(900,500),confirmButtons)
    confirmDefault = DefaultGroup()
    Text(2,"TEXT",(0,0,0),(800,450),confirmDefault,(475,50),(255,255,255),name="Text")

    fileFinderButtons = []
    fileFinderButtons.append(ButtonGroup())
    Button((125,50),2,"Back","Back",(255,255,255),(0,0,0),(75,850),fileFinderButtons[0])
    Button((125,50),2,"Load","Load",(255,255,255),(0,0,0),(1200,100),fileFinderButtons[0])
    Button((600,50),2,"",0,(255,255,255),(0,0,0),(800,200),fileFinderButtons[0])
    Button((600,50),2,"",1,(255,255,255),(0,0,0),(800,250),fileFinderButtons[0])
    Button((600,50),2,"",2,(255,255,255),(0,0,0),(800,300),fileFinderButtons[0])
    Button((600,50),2,"",3,(255,255,255),(0,0,0),(800,350),fileFinderButtons[0])
    Button((600,50),2,"",4,(255,255,255),(0,0,0),(800,400),fileFinderButtons[0])
    Button((600,50),2,"",5,(255,255,255),(0,0,0),(800,450),fileFinderButtons[0])
    Button((600,50),2,"",6,(255,255,255),(0,0,0),(800,500),fileFinderButtons[0])
    Button((600,50),2,"",7,(255,255,255),(0,0,0),(800,550),fileFinderButtons[0])
    Button((600,50),2,"",8,(255,255,255),(0,0,0),(800,600),fileFinderButtons[0])
    Button((600,50),2,"",9,(255,255,255),(0,0,0),(800,650),fileFinderButtons[0])
    Button((600,50),2,"",10,(255,255,255),(0,0,0),(800,700),fileFinderButtons[0])
    Button((600,50),2,"",11,(255,255,255),(0,0,0),(800,750),fileFinderButtons[0])
    fileFinderBox = BoxGroup()
    TextBox((600,50),2,"Search for file","File","Text",(255,255,255),(0,0,0),(800,100),fileFinderBox,True)
    # buttions that can be activated
    fileFinderButtons.append(ButtonGroup())
    Button((100,50),2,"Next","Next",(255,255,255),(0,0,0),(1050,850),fileFinderButtons[1])
    fileFinderButtons.append(ButtonGroup())
    Button((190,50),2,"Previous","Previous",(255,255,255),(0,0,0),(595,850),fileFinderButtons[2])

    return menuButtons, creatureCreatorButtons, creatureCreatorBox, creatureCreatorDefault, environmentCreatorButtons, environmentCreatorBox, environmentCreatorDefault, simulationCreatorButtons, simulationCreatorBox, simulationCreatorDefault, textEditorButtons, confirmButtons, confirmDefault, fileFinderButtons, fileFinderBox


def Menu():
    print("Menu")
    # Small Delay before buttions activate to stop accidental clicks
    screen.fill((0,0,0))
    menuButtons.draw(screen)
    pg.display.flip()
    time.sleep(0.5)
    timeDelay = 0
    # wait for buttion to be pressed
    while running:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        mousePos=pg.mouse.get_pos()

        pressed = menuButtons.update(mousePos) 

        # Detecting if there was a buttion pressed
        for press in pressed:
            if press != None:
            # Find what buttion was pressed
                if press == "Creature Creator":
                    CreatureCreator()
                    timeDelay = 0.5
                elif press == "Environment Creator":
                    EnvironmentCreator()
                    timeDelay = 0.5
                elif press == "Simulation Creator":
                    SimulationCreator()
                

        # clear screen and set backround colour
        screen.fill((0,0,0))
        # display the buttions
        menuButtons.draw(screen)

        pg.display.flip()
        if timeDelay:
            time.sleep(timeDelay)
            timeDelay = 0
        # run menu at 60 fps
        time.sleep(1/ FPS)
    

def CreatureCreator():
    print("Creature Creator")
    # Small Delay before buttions activate to stop accidental clicks
    screen.fill((0,0,0))
    creatureCreatorButtons.draw(screen)
    creatureCreatorBox.draw(screen)
    creatureCreatorDefault.draw(screen)
    pg.display.flip()
    time.sleep(0.5)
    timeDelay = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        
        mousePos=pg.mouse.get_pos()

        pressed = creatureCreatorButtons.update(mousePos) 
        timeDelay = creatureCreatorBox.update(mousePos)

        # Detecting if there was a buttion pressed
        for press in pressed:
            if press != None:
                # Find what buttion was pressed
                if press == "Exit":
                    return
                elif press == "Save":
                    data = creatureCreatorBox.getValues()
                    name = data.pop("Name")
                    SaveFile(name,"Creatures",data)
                elif press == "Load":
                    data = FileFinder("Creatures")
                    if data != None:
                        creatureCreatorBox.setValues(data)
                    timeDelay = 0.5
                elif press == "Delete":
                    data = creatureCreatorBox.getValues()
                    name = data.pop("Name")
                    if Confirm("Delete",f"Delete {name}?"):
                        deleteFile("Creatures",name)
                    timeDelay = 0.5

        # clear screen and set backround colour
        screen.fill((0,0,0))
        # display the buttions
        creatureCreatorButtons.draw(screen)
        creatureCreatorBox.draw(screen)
        creatureCreatorDefault.draw(screen)

        pg.display.flip()
        if timeDelay:
            time.sleep(timeDelay)
            timeDelay = 0
        # run at 60 fps
        time.sleep(1/ FPS)

def EnvironmentCreator():
    print("Environment Creator")
    # Small Delay before buttions activate to stop accidental clicks
    screen.fill((0,0,0))
    environmentCreatorButtons.draw(screen)
    environmentCreatorBox.draw(screen)
    environmentCreatorDefault.draw(screen)
    pg.display.flip()
    time.sleep(0.5)
    timeDelay = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        
        mousePos=pg.mouse.get_pos()

        pressed = environmentCreatorButtons.update(mousePos) 
        timeDelay = environmentCreatorBox.update(mousePos)

        # Detecting if there was a buttion pressed
        for press in pressed:
            if press != None:
                # Find what buttion was pressed
                if press == "Exit":
                    return
                elif press == "Save":
                    data = environmentCreatorBox.getValues()
                    name = data.pop("Name")
                    SaveFile(name,"Environment",data)
                elif press == "Load":
                    data = FileFinder("Environment")
                    if data != None:
                        environmentCreatorBox.setValues(data)
                    timeDelay = 0.5

        # clear screen and set backround colour
        screen.fill((0,0,0))
        # display the buttions
        environmentCreatorButtons.draw(screen)
        environmentCreatorBox.draw(screen)
        environmentCreatorDefault.draw(screen)

        pg.display.flip()
        if timeDelay:
            time.sleep(timeDelay)
            timeDelay = 0
        # run at 60 fps
        time.sleep(1/ FPS)

def SimulationCreator():
    print("Simulation Creator")
    # Small Delay before buttions activate to stop accidental clicks
    screen.fill((0,0,0))
    simulationCreatorButtons.draw(screen)
    simulationCreatorBox.draw(screen)
    simulationCreatorDefault.draw(screen)
    pg.display.flip()
    time.sleep(0.5)
    timeDelay = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        
        mousePos=pg.mouse.get_pos()

        pressed = simulationCreatorButtons.update(mousePos) 
        timeDelay = simulationCreatorBox.update(mousePos)

        # Detecting if there was a buttion pressed
        for press in pressed:
            if press != None:
                # Find what buttion was pressed
                if press == "Exit":
                    return
                elif press == "Save":
                    data = simulationCreatorBox.getValues()
                    name = data.pop("Name")
                    SaveFile(name,"Simulation",data)
                elif press == "Load":
                    data = FileFinder("Simulation")
                    if data != None:
                        simulationCreatorBox.setValues(data)
                    timeDelay = 0.5

        # clear screen and set backround colour
        screen.fill((0,0,0))
        # display the buttions
        simulationCreatorButtons.draw(screen)
        simulationCreatorBox.draw(screen)
        simulationCreatorDefault.draw(screen)

        pg.display.flip()
        if timeDelay:
            time.sleep(timeDelay)
            timeDelay = 0
        # run at 60 fps
        time.sleep(1/ FPS)

def FileFinder(valueType):
    print("File Finder")
    timeDelay = 0
    # Get names for buttions
    fileNames = folderRead(f"Assets/{valueType}")
    page = 0
    # convert the names from a list to a dict
    buttionText = {}
    for i in range(len(fileNames[page])):
        buttionText[i] = fileNames[page][i]
    amountOfPages = len(fileNames)-1
    # change the buttion text to match
    fileFinderButtons[0].setText(buttionText)
    # Small Delay before buttions activate to stop accidental clicks
    screen.fill((0,0,0))
    fileFinderButtons[0].draw(screen)
    fileFinderBox.draw(screen)
    if amountOfPages > page:
        fileFinderButtons[1].draw(screen)
    pg.display.flip()
    time.sleep(0.5)
    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        
        mousePos=pg.mouse.get_pos()

        pressed = fileFinderButtons[0].update(mousePos) 
        if amountOfPages > page:
            pressed += fileFinderButtons[1].update(mousePos) 
        if page > 0:
            pressed += fileFinderButtons[2].update(mousePos) 
        timeDelay = fileFinderBox.update(mousePos)

        # Detecting if there was a buttion pressed
        for press in pressed:
            if press != None:
                # Find what buttion was pressed
                if press == "Back":
                    return None
                elif press == "Load":
                    data = fileFinderBox.getValues()
                    name = data.pop("File")
                    if name != "Search for file":
                        data = LoadFile(name,valueType)
                        if data != None:
                            return data
                elif press == "Next":
                    page += 1
                    for i in range(0,12):
                        if i < len(fileNames[page]):
                            buttionText[i] = fileNames[page][i]
                        else:
                            buttionText[i] = ""
                    amountOfPages = len(fileNames)-1
                    # change the buttion text to match
                    fileFinderButtons[0].setText(buttionText)
                    timeDelay = 0.5
                elif press == "Previous":
                    page -= 1
                    for i in range(0,12):
                        if i < len(fileNames[page]):
                            buttionText[i] = fileNames[page][i]
                        else:
                            buttionText[i] = ""
                    amountOfPages = len(fileNames)-1
                    # change the buttion text to match
                    fileFinderButtons[0].setText(buttionText)
                    timeDelay = 0.5
                else:
                    name = fileNames[page][press]
                    data = LoadFile(name,valueType)
                    if data != None:
                        return data

        # clear screen and set backround colour
        screen.fill((0,0,0))
        # display the buttions
        fileFinderButtons[0].draw(screen)
        fileFinderBox.draw(screen)
        if amountOfPages > page:
            fileFinderButtons[1].draw(screen)
        if page > 0:
            fileFinderButtons[2].draw(screen)
        pg.display.flip()
        if timeDelay:
            time.sleep(timeDelay)
            timeDelay = 0
        # run at 60 fps
        time.sleep(1/ FPS)

def NumEditor(number=""):
    print("Num Editor")
    numbers = str(number)
    # Small Delay before buttions activate to stop accidental clicks
    screen.fill((0,0,0))
    SpriteRender((400,50),(255,255,255),(800,450),screen)
    TextRender(numbers,2,(0,0,0),(800,450),screen)
    textEditorButtons.draw(screen)
    pg.display.flip()
    time.sleep(0.5)
    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                # detect if the key pressed was a number
                elif event.key >= 48 and event.key <=57:
                    number = event.key - 48
                    # add number to the string
                    numbers += str(number)
                    # check for to many numbers
                    if len(numbers) > 15:
                        numbers = numbers[:-1]
                elif event.key == pg.K_BACKSPACE:
                    # remove number
                    numbers = numbers[:-1]
                elif event.key == 46 and "." not in numbers:
                    numbers += "."
                    if len(numbers) > 15:
                        numbers = numbers[:-1]
            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        mousePos=pg.mouse.get_pos()

        pressed = textEditorButtons.update(mousePos) 
        # Detecting if there was a buttion pressed
        for press in pressed:
            if press != None:
                # Find what buttion was pressed
                if press == "Confirm":
                    return numbers
                elif press == "Cancel":
                    return None

        # clear screen and set backround colour
        screen.fill((0,0,0))
        # display numbers
        SpriteRender((400,50),(255,255,255),(800,450),screen)
        TextRender(numbers,2,(0,0,0),(800,450),screen)
        # display the buttions
        textEditorButtons.draw(screen)

        pg.display.flip()
        # run at 60 fps
        time.sleep(1/ FPS)

def TextEditor(text=""):
    print("Text Editor")
    # Small Delay before buttions activate to stop accidental clicks
    screen.fill((0,0,0))
    SpriteRender((600,50),(255,255,255),(800,450),screen)
    TextRender(text,2,(0,0,0),(800,450),screen)
    textEditorButtons.draw(screen)
    pg.display.flip()
    time.sleep(0.5)
    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                # detect if the key pressed was a letter
                elif event.key >= 97 and event.key <=123:
                    letter = LETTERS[event.key - 97]
                    # add letter to the string and check if it should be a upper case or lower case
                    # check if the correct mods for uppercase is pressed
                    if pg.key.get_mods() in [4097,4098,4099,12288,1,2,3,8192]:
                        text += letter.upper()
                    else:
                        text += letter
                    # check for to many letters
                    if len(text) > 15:
                        text = text[:-1]
                elif event.key == pg.K_BACKSPACE:
                    # remove letter
                    text = text[:-1]
                elif event.key == pg.K_SPACE:
                    text += " "
                    if len(text) > 15:
                        text = text[:-1]
            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        mousePos=pg.mouse.get_pos()

        pressed = textEditorButtons.update(mousePos) 
        # Detecting if there was a buttion pressed
        for press in pressed:
            if press != None:
                # Find what buttion was pressed
                if press == "Confirm":
                    return text
                elif press == "Cancel":
                    return None
        
        # clear screen and set backround colour
        screen.fill((0,0,0))
        # display text
        SpriteRender((600,50),(255,255,255),(800,450),screen)
        TextRender(text,2,(0,0,0),(800,450),screen)
        # display the buttions
        textEditorButtons.draw(screen)

        pg.display.flip()
        # run at 60 fps
        time.sleep(1/ FPS)

def Confirm(buttionText = "Confirm",text = "auto"):
    print("Confirm")
    # Small Delay before buttions activate to stop accidental clicks
    if text == "auto":
        text = f"{buttionText}"
    data = {"Confirm":buttionText,"Text":text}
    confirmButtons.setText(data)
    confirmDefault.setText(data)
    screen.fill((0,0,0))
    confirmDefault.draw(screen)
    confirmButtons.draw(screen)
    pg.display.flip()
    time.sleep(0.5)
    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        mousePos=pg.mouse.get_pos()

        pressed = confirmButtons.update(mousePos) 
        # Detecting if there was a buttion pressed
        for press in pressed:
            if press != None:
                # Find what buttion was pressed
                if press == "Confirm":
                    return True
                elif press == "Cancel":
                    return False
        
        # clear screen and set backround colour
        screen.fill((0,0,0))
        # display the buttions
        confirmDefault.draw(screen)
        confirmButtons.draw(screen)

        pg.display.flip()
        # run at 60 fps
        time.sleep(1/ FPS)

def SaveFile(name,type,dictionary):
    fileSaved = False
    fileOpen = False
    try:
        # try and save file will error if there is a file with that name already
        file = open(f"Assets/{type}/{name}.txt","x")
        fileOpen = True
    except:
        # the file exists, asking user if they want to overwrite the data
        if Confirm("Overwrite","This file already exists"):
            # overwriting file
            file = open(f"Assets/{type}/{name}.txt","w")
            fileOpen = True
    
    if fileOpen:
        # convert dictionary to string so it can be saved
        data = ""
        for key in dictionary:
            data += f"{key}:{dictionary[key]}\n"
        # save data to file
        file.write(data)
        file.close()
        fileSaved = True
    
    if fileSaved:
        # display message that file has been saved
        message(f"File saved as {name}")
    else:
        # display message that file has not been saved
        message("File has not been saved")

def LoadFile(name,type):
    try:
        # try to open file
        file = open(f"Assets/{type}/{name}.txt","r")
        data = file.read()
        file.close()
    except:
        # no file at location will cause an error
        message("File could not be found")
        return None
    
    # convert the files text back in to a dictionary
    data = data.split("\n")
    dictionary = {'Name':name}
    for value in data:
        value = value.split(":")
        if value != ['']:
            key = value[0]
            value = value[1]
            dictionary[key] = value
    # file loaded message
    message(f"File {name} loaded")
    return dictionary

def folderRead(folder):
    names = [[]]
    files = os.listdir(folder)
    files.sort()
    for file in files:
        if len(names[len(names)-1]) < 12:
            names[len(names)-1].append(file[:-4])
        else:
            names.append([])
            names[len(names)-1].append(file[:-4])
    return(names)

def deleteFile(folder,name):
    try:
        open(f"Assets/{folder}/{name}.txt","r")
        os.remove(f"Assets/{folder}/{name}.txt")
    except:
        message("File could not be deleted")

def message(text, length = 800,timeDelay = 1):
    SpriteRender((length,50),(255,255,255),(800,450),screen)
    TextRender(text,2,(0,0,0),(800,450),screen)
    pg.display.flip()
    time.sleep(timeDelay) 

print("Seting Up")
# General setup
pg.init()
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
screen = pg.display.set_mode((0,0),pg.FULLSCREEN, display=0)
pg.display.set_caption("NEA")
clock = pg.time.Clock()
running = True




# Menu Settup



menuButtons, creatureCreatorButtons, creatureCreatorBox, creatureCreatorDefault, environmentCreatorButtons, environmentCreatorBox, environmentCreatorDefault, simulationCreatorButtons, simulationCreatorBox, simulationCreatorDefault, textEditorButtons, confirmButtons, confirmDefault, fileFinderButtons, fileFinderBox = setup()
while running:
    Menu()
    print("???")
    clock.tick()
    pg.display.flip()