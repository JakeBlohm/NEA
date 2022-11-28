import sys
import time
import pyautogui
import os
import pygame as pg
import simulation

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
print(pyautogui.size())
SCALE = SCREEN_WIDTH / 1600
print(SCALE)
FPS = 60
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

class ButtonGroup(pg.sprite.Group):
    """A group of Buttons"""
    def update(self, mousePos: tuple, mClick: bool) -> list:
        """Gets a list of all buttons pressed within the ButtonGroup
        
        Returns:
            [Button.name, Button.name, ...] list of all button names pressed."""
        pressed = []
        buttons = self.sprites()
        for button in buttons:
            pressed.append(button.update(mousePos, mClick))
        return pressed

    def draw(self, screen: pg.Surface) -> None:
        """Draws all buttons within the ButtonGroup"""
        buttons = self.sprites()
        for button in buttons:
            button.draw(screen)
        
    def setText(self, data: dict) -> None:
        """Sets text of all buttons within the ButtonGroup"""
        buttons = self.sprites()
        for button in buttons:
            button.setText(data)


class Button(pg.sprite.Sprite):
    """A pressable button
    
    Takes:
        size: tuple(int,int), textSize: int, screenText: str, name: str,
        colour: tuple(int,int.int), textColour: tuple(int,int,int),
        pos: tuple(int,int), group: ButtonGroup"""

    def __init__(self, size: tuple[int,int],
                textSize: int, screenText: str, 
                name: str, colour: tuple[int,int,int],
                textColour: tuple[int,int,int], 
                pos: tuple[int,int], group: ButtonGroup) -> None:

        print("Creating button")
        # Create button
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

    def update(self, mousePos: tuple[int,int], mClick: bool) -> str:
        """Highlights button on mouse over, returns name when clicked.
        
        Returns:
            Button.name: string"""
        # detect if the mouse is on the button
        if self.rect.collidepoint(mousePos):
            # add highlight effect
            self.image.fill((self.colour[0]-50,self.colour[1]-50,self.colour[2]-50))
            self.highlight = True
            # detect when the mouse button is pressed
            if mClick:
                return self.name

        elif self.highlight:
            # remove highlight effect
            self.image.fill(self.colour)
            self.highlight = False

    def draw(self, screen: pg.Surface) -> None:
        """Draws the Button to the passed screen"""
        # display the button then text
        screen.blit(self.image,self.rect)
        screen.blit(self.text,self.rect)
    
    def setText(self, data: dict) -> None:
        """Sets the text of the button to keyed data in a passed dict"""
        if self.name in data:
            self.screenText = data[self.name]
            self.text = self.font.render(self.screenText, 0, pg.Color(self.textColour))


class BoxGroup(pg.sprite.Group):
    def update(self, mousePos: tuple[int,int], mClick: bool) -> float:
        boxes = self.sprites()
        for box in boxes:
            box.update(mousePos, mClick)


    def draw(self, screen: pg.Surface) -> None:
        boxes = self.sprites()
        for box in boxes:
            box.draw(screen)

    def getValues(self) -> dict:
        dictionary = {}
        boxes = self.sprites()
        for box in boxes:
            name,value=(box.getValue())
            dictionary[name] = value
        return dictionary

    def setValues(self, data: dict) -> None:
        boxes = self.sprites()
        for box in boxes:
            box.setValue(data)


class TextBox(pg.sprite.Sprite):
    def __init__(self, size: tuple[int,int], 
                textSize: tuple[int,int], startValue: str, 
                name: str, valueType: str,
                colour: tuple[int,int,int], textColour: tuple[int,int,int], 
                pos: tuple[int,int], group: BoxGroup, 
                deleteValueOnClick: bool=False) -> None:

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
    
    def update(self, mousePos: tuple[int,int], mClick: bool) -> float:
        # detect if the mouse is on the button
        if self.rect.collidepoint(mousePos):
            # add highlight effect
            self.image.fill((self.colour[0]-50,self.colour[1]-50,self.colour[2]-50))
            self.highlight = True
            # detect when the mouse button is pressed
            if mClick:
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

        elif self.highlight:
            # remove highlight effect
            self.image.fill(self.colour)
            self.highlight = False

    def draw(self, screen: pg.Surface) -> None:
        # display the button then text
        screen.blit(self.image,self.rect)
        screen.blit(self.text,self.rect)
    
    def getValue(self) -> tuple[str, int]:
        return self.name, self.value
    
    def setValue(self, data: dict) -> None:
        if self.name in data:
            self.value = data[self.name]
            self.text = self.font.render(self.value, 0, pg.Color(self.textColour))


class TickBox(pg.sprite.Sprite):
    def __init__(self, size: tuple[int,int], 
                textSize: tuple[int,int], startValue: bool, 
                name: str, colour: tuple[int,int,int],
                textColour: tuple[int,int,int], pos: tuple[int,int], 
                group: BoxGroup) -> None:

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
    
    def update(self, mousePos: tuple[int,int], mClick: bool):
        # detect if the mouse is on the button
        if self.rect.collidepoint(mousePos):
            # add highlight effect
            self.image.fill((self.textColour[0]-50,self.textColour[1]-50,self.textColour[2]-50))
            self.highlight = True
            # detect when the mouse button is pressed
            if mClick:
                self.value = not self.value

        elif self.highlight:
            # remove highlight effect
            self.image.fill(self.textColour)
            self.highlight = False

    def draw(self, screen: pg.Surface) -> None:
        # display the button then text
        screen.blit(self.image,self.rect)
        if self.value:
            screen.blit(self.cutout,self.rectCutout)
        screen.blit(self.text,self.pos)
    
    def getValue(self) -> tuple[str, int]:
        return self.name, self.value
    
    def setValue(self, data: dict) -> None:
        if self.name in data:
            self.value = data[self.name]


class MultiBox(pg.sprite.Sprite):
    def __init__(self,quantity: int,size: tuple[int,int],textSize:int,position: tuple[int,int],group) -> None:
        pg.sprite.Sprite.__init__(self)
        print("Creating multi box")
        # Create multiBox
        group = group
        group.add(self)
        self.creaturelist = []
        self.buttonList = [[]]
        self.quantity = quantity
        self.page = 0

        self.multiButtons = []
        self.multiButtons.append(ButtonGroup())
        for i in range(0,quantity):
            Button((size[0],size[1]),textSize,"",i,(255,255,255),(0,0,0),(position[0]+size[0]*0.5,(position[1]+size[1]*0.5)+size[1]*i),self.multiButtons[0])

        Button((size[0],size[1]),textSize,"Select Creature","Select Creature",(255,255,255),(0,0,0),(position[0]+size[0]*0.5,(position[1]+size[1]*0.5)+size[1]*(i+1)),self.multiButtons[0])

        # buttons that can be activated
        self.multiButtons.append(ButtonGroup())
        Button((size[0]*0.5,size[1]),textSize,"Next","Next",(255,255,255),(0,0,0),(position[0]+size[0]*0.75,(position[1]+size[1]/2)+size[1]*(i+2)),self.multiButtons[1])
        self.multiButtons.append(ButtonGroup())
        Button((size[0]*0.5,size[1]),textSize,"Prev","Prev",(255,255,255),(0,0,0),(position[0]+size[0]*0.25,(position[1]+size[1]/2)+size[1]*(i+2)),self.multiButtons[2])

    
    def update(self, mousePos: tuple[int,int], mClick: bool) -> float:
    
        pressed = self.multiButtons[0].update(mousePos,mClick)
        if "Select Creature" in pressed:
            newName = FileFinder("Creatures")
            if newName:
                newName = newName["Name"]
                if newName not in self.creaturelist:
                    self.creaturelist.append(newName)
                    self.updateButtons()
        
        if len(self.buttonList)-1 > self.page:
            pressed = self.multiButtons[1].update(mousePos,mClick)
            if "Next" in pressed:
                self.page += 1
                self.updateButtons()
        

        elif self.page > 0:
            pressed = self.multiButtons[2].update(mousePos,mClick)
            if "Prev" in pressed:
                self.page -= 1
                self.updateButtons()

        
        



        
    
    def updateButtons(self):
        self.buttonList = [[]]
        for creature in self.creaturelist:
            if len(self.buttonList[-1]) >= self.quantity:
                self.buttonList.append([creature])
            else:
                self.buttonList[-1].append(creature)
        buttonText = {}
        for i in range(len(self.buttonList[self.page])):
            buttonText[i] = self.buttonList[self.page][i]
        for j in range(i+1 ,self.quantity):
            buttonText[j] = ""
        self.amountOfPages = len(self.buttonList)-1
        # change the button text to match
        self.multiButtons[0].setText(buttonText)




        
        


    def draw(self, screen: pg.Surface) -> None:
        # display the button then text
        self.multiButtons[0].draw(screen)
        if len(self.buttonList)-1 > self.page:
            pressed = self.multiButtons[1].draw(screen)
        
        elif self.page > 0:
            pressed = self.multiButtons[2].draw(screen)
    
    def getValue(self) -> tuple[str, int]:
        return self.name, self.value
    
    def setValue(self, data: dict) -> None:
        if self.name in data:
            self.value = data[self.name]
            self.text = self.font.render(self.value, 0, pg.Color(self.textColour))


class DefaultGroup(pg.sprite.Group):
    def draw(self, screen: pg.Surface) -> None:
        sprites = self.sprites()
        for sprite in sprites:
            sprite.draw(screen)

    def setText(self, data: dict) -> None:
        sprites = self.sprites()
        for sprite in sprites:
            sprite.setText(data)


class Text(pg.sprite.Sprite):
    def __init__(self, textSize: tuple[int,int], 
                text: str, textColour : tuple[int,int,int], 
                pos: tuple[int,int], group: DefaultGroup,
                size: int=None, colour: tuple[int,int,int]=None,
                alignment: str="center", name: str=None) -> None:

        print("Creating Text")
        # Create button
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

    def draw(self, screen: pg.Surface) -> None:
        # display the button then text
        if self.backround:
            screen.blit(self.image,self.rect)
        screen.blit(self.text,self.rect)
    
    def setText(self, data: dict) -> None:
        if self.name in data:
            text = data[self.name]
            self.text = self.font.render(text, 0, pg.Color(self.textColour))
    

def TextRender(text: str, scale: float, 
                colour: tuple[int,int,int], pos: tuple[int,int], 
                screen: pg.Surface) -> None:

    font = pg.font.SysFont('Arial', int(24*SCALE*scale))
    text = font.render(text, 0, pg.Color(colour))
    rect = text.get_rect(center = (pos[0]*SCALE,pos[1]*SCALE))
    screen.blit(text,rect)

def SpriteRender(size: tuple[int,int], colour: tuple[int,int,int], 
                pos: tuple[int,int], screen: pg.Surface) -> None:

    image = pg.Surface([size[0]*SCALE, size[1]*SCALE])
    image.fill(colour)
    rect = image.get_rect(center = (pos[0]*SCALE,pos[1]*SCALE))
    screen.blit(image,rect)

def setup() -> tuple[ButtonGroup,
                    ButtonGroup,BoxGroup,DefaultGroup,
                    ButtonGroup,BoxGroup,DefaultGroup,
                    ButtonGroup,BoxGroup,DefaultGroup,
                    ButtonGroup,
                    ButtonGroup,DefaultGroup,
                    ButtonGroup,BoxGroup]:

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
    TextBox((200,25),1,"1","Size","Number",(255,255,255),(0,0,0),(300,100),creatureCreatorBox,True)
    TextBox((200,25),1,"1","SizeEM","Number",(255,255,255),(0,0,0),(550,100),creatureCreatorBox,True)
    TextBox((200,25),1,"1","Sight","Number",(255,255,255),(0,0,0),(300,150),creatureCreatorBox,True)
    TextBox((200,25),1,"1","SightEM","Number",(255,255,255),(0,0,0),(550,150),creatureCreatorBox,True)
    TextBox((200,25),1,"45","FOV","Number",(255,255,255),(0,0,0),(300,200),creatureCreatorBox,True)
    TextBox((200,25),1,"1","FOVEM","Number",(255,255,255),(0,0,0),(550,200),creatureCreatorBox,True)
    TickBox((200,25),1,False,"Eats Berrys",(0,0,0),(255,255,255),(300,250),creatureCreatorBox)
    creatureCreatorDefault = DefaultGroup()
    Text(1,"Name",(255,255,255),(1400,25),creatureCreatorDefault)
    Text(1,"Base Value",(255,255,255),(300,25),creatureCreatorDefault)
    Text(1,"Evolution Modifier",(255,255,255),(550,25),creatureCreatorDefault)
    Text(1,"Speed",(255,255,255),(0,50),creatureCreatorDefault,alignment="left")
    Text(1,"Size",(255,255,255),(0,100),creatureCreatorDefault,alignment="left")
    Text(1,"Sight",(255,255,255),(0,150),creatureCreatorDefault,alignment="left")
    Text(1,"FOV",(255,255,255),(0,200),creatureCreatorDefault,alignment="left")

    environmentCreatorButtons = ButtonGroup()
    Button((100,50),2,"Exit","Exit",(255,255,255),(0,0,0),(75,850),environmentCreatorButtons)
    Button((125,50),2,"Save","Save",(255,255,255),(0,0,0),(1500,850),environmentCreatorButtons)
    Button((125,50),2,"Load","Load",(255,255,255),(0,0,0),(1350,850),environmentCreatorButtons)
    environmentCreatorBox = BoxGroup()
    TextBox((300,25),1,"Name","Name","Text",(255,255,255),(0,0,0),(1400,50),environmentCreatorBox,True)
    TextBox((200,25),1,"1","SpeedFD","Number",(255,255,255),(0,0,0),(800,50),environmentCreatorBox,True)
    TextBox((200,25),1,"1","HealthFD","Number",(255,255,255),(0,0,0),(800,100),environmentCreatorBox,True)
    TextBox((200,25),1,"1","VisionDistanceFD","Number",(255,255,255),(0,0,0),(800,150),environmentCreatorBox,True)
    TextBox((200,25),1,"1","FOVFD","Number",(255,255,255),(0,0,0),(800,200),environmentCreatorBox,True)
    environmentCreatorDefault = DefaultGroup()
    Text(1,"Name",(255,255,255),(1400,25),environmentCreatorDefault)
    Text(1,"Food Drain",(255,255,255),(800,25),environmentCreatorDefault)
    Text(1,"Creatures",(255,255,255),(75,25),environmentCreatorDefault)

    simulationCreatorButtons = ButtonGroup()
    Button((100,50),2,"Exit","Exit",(255,255,255),(0,0,0),(75,850),simulationCreatorButtons)
    Button((125,50),2,"Save","Save",(255,255,255),(0,0,0),(1500,850),simulationCreatorButtons)
    Button((125,50),2,"Load","Load",(255,255,255),(0,0,0),(1350,850),simulationCreatorButtons)
    Button((125,50),2,"Load","Load",(255,255,255),(0,0,0),(1350,850),simulationCreatorButtons)
    Button((280,50),2,"Run Simulation","Run Simulation",(255,255,255),(0,0,0),(800,850),simulationCreatorButtons)
    
    simulationCreatorBox = BoxGroup()
    TextBox((300,25),1,"Name","Name","Text",(255,255,255),(0,0,0),(1400,50),simulationCreatorBox,True)
    MultiBox(2,(300,50),2,(10,50),simulationCreatorBox)
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
    # buttons that can be activated
    fileFinderButtons.append(ButtonGroup())
    Button((100,50),2,"Next","Next",(255,255,255),(0,0,0),(1050,850),fileFinderButtons[1])
    fileFinderButtons.append(ButtonGroup())
    Button((190,50),2,"Previous","Previous",(255,255,255),(0,0,0),(595,850),fileFinderButtons[2])

    return (
        menuButtons, 
        creatureCreatorButtons, 
        creatureCreatorBox, 
        creatureCreatorDefault, 
        environmentCreatorButtons, 
        environmentCreatorBox, 
        environmentCreatorDefault, 
        simulationCreatorButtons, 
        simulationCreatorBox, 
        simulationCreatorDefault, 
        textEditorButtons, 
        confirmButtons, 
        confirmDefault, 
        fileFinderButtons, 
        fileFinderBox
        )

def menu() -> None:
    print("Menu")
    screen.fill((0,0,0))
    menuButtons.draw(screen)
    pg.display.flip()
    # wait for button to be pressed
    while running:
        mClick = False
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mClick = True

        mousePos=pg.mouse.get_pos()

        pressed = menuButtons.update(mousePos,mClick) 

        # Detecting if there was a button pressed
        for press in pressed:
            if press != None:
            # Find what button was pressed
                if press == "Creature Creator":
                    CreatureCreator()
                  
                elif press == "Environment Creator":
                    EnvironmentCreator()

                elif press == "Simulation Creator":
                    SimulationCreator()
                

        # clear screen and set background colour
        screen.fill((0,0,0))
        # display the buttons
        menuButtons.draw(screen)

        pg.display.flip()
        
        # run menu at set fps
        time.sleep(1/ FPS)
    
def CreatureCreator() -> None:
    print("Creature Creator")
   
    while True:
        mClick = False
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mClick = True

        
        mousePos=pg.mouse.get_pos()

        pressed = creatureCreatorButtons.update(mousePos, mClick) 
        creatureCreatorBox.update(mousePos, mClick)

        # Detecting if there was a button pressed
        for press in pressed:
            if press != None:
                # Find what button was pressed
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
                    
                elif press == "Delete":
                    data = creatureCreatorBox.getValues()
                    name = data.pop("Name")
                    if Confirm("Delete",f"Delete {name}?"):
                        deleteFile("Creatures",name)
                    

        # clear screen and set background colour
        screen.fill((0,0,0))
        # display the buttons
        creatureCreatorButtons.draw(screen)
        creatureCreatorBox.draw(screen)
        creatureCreatorDefault.draw(screen)

        pg.display.flip()
        # run at set fps
        time.sleep(1/ FPS)

def EnvironmentCreator() -> None:
    print("Environment Creator")

    while True:
        mClick = False
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mClick = True

        
        mousePos=pg.mouse.get_pos()

        pressed = environmentCreatorButtons.update(mousePos, mClick) 
        environmentCreatorBox.update(mousePos, mClick)

        # Detecting if there was a button pressed
        for press in pressed:
            if press != None:
                # Find what button was pressed
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

        # clear screen and set background colour
        screen.fill((0,0,0))
        # display the buttons
        environmentCreatorButtons.draw(screen)
        environmentCreatorBox.draw(screen)
        environmentCreatorDefault.draw(screen)

        pg.display.flip()

        # run at set fps
        time.sleep(1/ FPS)

def SimulationCreator() -> None:
    print("Simulation Creator")

    while True:
        mClick = False
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mClick = True
        
        mousePos=pg.mouse.get_pos()

        pressed = simulationCreatorButtons.update(mousePos, mClick) 
        simulationCreatorBox.update(mousePos, mClick)

        # Detecting if there was a button pressed
        for press in pressed:
            if press != None:
                # Find what button was pressed
                if press == "Exit":
                    return
                elif press == "Run Simulation":
                    sim = simulation.Simulation(screen,[["name",1000,[[10,1],[10,1],[1000000,1],[360,1],[20,1]]]],[[100,10,20],[0.001,0.0,0.0,0.0]])
                    sim.run()
                elif press == "Save":
                    data = simulationCreatorBox.getValues()
                    name = data.pop("Name")
                    SaveFile(name,"Simulation",data)
                elif press == "Load":
                    data = FileFinder("Simulation")
                    if data != None:
                        simulationCreatorBox.setValues(data)

        # clear screen and set background colour
        screen.fill((0,0,0))
        # display the buttons
        simulationCreatorButtons.draw(screen)
        simulationCreatorBox.draw(screen)
        simulationCreatorDefault.draw(screen)

        pg.display.flip()
        # run at set fps
        time.sleep(1/ FPS)

def FileFinder(valueType: str) -> dict:
    print("File Finder")
    # Get names for buttons
    fileNames = folderRead(f"assets/{valueType}")
    page = 0
    # convert the names from a list to a dict
    buttonText = {}
    for i in range(len(fileNames[page])):
        buttonText[i] = fileNames[page][i]
    amountOfPages = len(fileNames)-1
    # change the button text to match
    fileFinderButtons[0].setText(buttonText)
    
    while True:
        mClick = False
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mClick = True
        
        mousePos=pg.mouse.get_pos()

        pressed = fileFinderButtons[0].update(mousePos, mClick) 
        if amountOfPages > page:
            pressed += fileFinderButtons[1].update(mousePos, mClick) 
        if page > 0:
            pressed += fileFinderButtons[2].update(mousePos, mClick) 
        fileFinderBox.update(mousePos, mClick)

        # Detecting if there was a button pressed
        for press in pressed:
            if press != None:
                # Find what button was pressed
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
                            buttonText[i] = fileNames[page][i]
                        else:
                            buttonText[i] = ""
                    amountOfPages = len(fileNames)-1
                    # change the button text to match
                    fileFinderButtons[0].setText(buttonText)
                elif press == "Previous":
                    page -= 1
                    for i in range(0,12):
                        if i < len(fileNames[page]):
                            buttonText[i] = fileNames[page][i]
                        else:
                            buttonText[i] = ""
                    amountOfPages = len(fileNames)-1
                    # change the button text to match
                    fileFinderButtons[0].setText(buttonText)
                else:
                    name = fileNames[page][press]
                    data = LoadFile(name,valueType)
                    if data != None:
                        return data

        # clear screen and set background colour
        screen.fill((0,0,0))
        # display the buttons
        fileFinderButtons[0].draw(screen)
        fileFinderBox.draw(screen)
        if amountOfPages > page:
            fileFinderButtons[1].draw(screen)
        if page > 0:
            fileFinderButtons[2].draw(screen)
        pg.display.flip()
        # run at set fps
        time.sleep(1/ FPS)

def NumEditor(number: str="") -> str:
    print("Num Editor")
    numbers = str(number)
    
    while True:
        mClick = False
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
            elif event.type == pg.MOUSEBUTTONDOWN:
                mClick = True

        mousePos=pg.mouse.get_pos()

        pressed = textEditorButtons.update(mousePos, mClick) 
        # Detecting if there was a button pressed
        for press in pressed:
            if press != None:
                # Find what button was pressed
                if press == "Confirm":
                    return numbers
                elif press == "Cancel":
                    return None

        # clear screen and set background colour
        screen.fill((0,0,0))
        # display numbers
        SpriteRender((400,50),(255,255,255),(800,450),screen)
        TextRender(numbers,2,(0,0,0),(800,450),screen)
        # display the buttons
        textEditorButtons.draw(screen)

        pg.display.flip()
        # run at 60 fps
        time.sleep(1/ FPS)

def TextEditor(text: str="") -> str:
    print("Text Editor")

    while True:
        mClick = False
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
            elif event.type == pg.MOUSEBUTTONDOWN:
                mClick = True

        mousePos=pg.mouse.get_pos()

        pressed = textEditorButtons.update(mousePos, mClick) 
        # Detecting if there was a button pressed
        for press in pressed:
            if press != None:
                # Find what button was pressed
                if press == "Confirm":
                    return text
                elif press == "Cancel":
                    return None
        
        # clear screen and set background colour
        screen.fill((0,0,0))
        # display text
        SpriteRender((600,50),(255,255,255),(800,450),screen)
        TextRender(text,2,(0,0,0),(800,450),screen)
        # display the buttons
        textEditorButtons.draw(screen)

        pg.display.flip()
        # run at 60 fps
        time.sleep(1/ FPS)

def Confirm(buttonText: str="Confirm", text: str="auto") -> bool:
    print("Confirm")
    if text == "auto":
        text = f"{buttonText}"
    data = {"Confirm":buttonText,"Text":text}
    confirmButtons.setText(data)
    confirmDefault.setText(data)
    
    while True:
        mClick = False
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mClick = True

        mousePos=pg.mouse.get_pos()

        pressed = confirmButtons.update(mousePos, mClick) 
        # Detecting if there was a button pressed
        for press in pressed:
            if press != None:
                # Find what button was pressed
                if press == "Confirm":
                    return True
                elif press == "Cancel":
                    return False
        
        # clear screen and set background colour
        screen.fill((0,0,0))
        # display the buttons
        confirmDefault.draw(screen)
        confirmButtons.draw(screen)

        pg.display.flip()
        # run at 60 fps
        time.sleep(1/ FPS)

def SaveFile(name: str, type: str, dictionary: dict) -> None:
    fileSaved = False
    fileOpen = False
    try:
        # try and save file will error if there is a file with that name already
        file = open(f"assets/{type}/{name}.txt","x")
        fileOpen = True
    except:
        # the file exists, asking user if they want to overwrite the data
        if Confirm("Overwrite","This file already exists"):
            # overwriting file
            file = open(f"assets/{type}/{name}.txt","w")
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

def LoadFile(name: str, type: str) -> dict:
    try:
        # try to open file
        file = open(f"assets/{type}/{name}.txt","r")
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

def folderRead(folder: str) -> list:
    names = [[]]
    files = os.listdir(folder)
    files.sort()
    for file in files:
        if len(names[len(names)-1]) < 12:
            names[len(names)-1].append(file[:-4])
        else:
            names.append([])
            names[len(names)-1].append(file[:-4])
    return names

def deleteFile(folder: str, name: str) -> None:
    try:
        open(f"assets/{folder}/{name}.txt","r")
        os.remove(f"assets/{folder}/{name}.txt")
    except:
        message("File could not be deleted")

def message(text: str, length: int=800, timeDelay: int=1) -> None:
    SpriteRender((length,50),(255,255,255),(800,450),screen)
    TextRender(text,2,(0,0,0),(800,450),screen)
    pg.display.flip()
    time.sleep(timeDelay) 

print("Seting Up")
# General setup
pg.init()
screen = pg.display.set_mode((0,0),pg.FULLSCREEN, display=0)
pg.display.set_caption("NEA")
clock = pg.time.Clock()
running = True

# Menu Settup

(
    menuButtons, creatureCreatorButtons, 
    creatureCreatorBox, creatureCreatorDefault, 
    environmentCreatorButtons, environmentCreatorBox, 
    environmentCreatorDefault, simulationCreatorButtons, 
    simulationCreatorBox, simulationCreatorDefault, 
    textEditorButtons, confirmButtons, 
    confirmDefault, fileFinderButtons,
    fileFinderBox) = setup()

while running:
    menu()
    print("???")
    clock.tick()
    pg.display.flip()