import pygame as pg
from settings import SCALE
from functions import message
from advFunctions import FileFinder
from baseFunctions import NumEditor
from baseClasses import ButtonGroup,Button


class MultiBox(pg.sprite.Sprite):
    def __init__(self,name,quantity: int,size: tuple[int,int],textSize:int,position: tuple[int,int],group,numbers = False) -> None:
        pg.sprite.Sprite.__init__(self)
        print("Creating multi box")
        # Create multiBox
        group = group
        group.add(self)
        self.nameDic = {}
        self.buttonList = [[]]
        self.quantity = quantity
        self.page = 0
        self.name = name

        self.multiButtons = []
        self.multiButtons.append(ButtonGroup())

        if numbers:
            sizeMod = 0.75
            self.multiNumB = ButtonGroup()
            for i in range(0,quantity):
                Button((size[0]*0.25,size[1]),textSize,"",i,(255,255,255),(0,0,0),(position[0]+size[0]*0.875,(position[1]+size[1]*0.5)+size[1]*i),self.multiNumB)

        else:
            sizeMod = 1

        for i in range(0,quantity):
            Button((size[0]*sizeMod,size[1]),textSize,"",i,(255,255,255),(0,0,0),(position[0]+size[0]*0.5*sizeMod,(position[1]+size[1]*0.5)+size[1]*i),self.multiButtons[0])

        Button((size[0],size[1]),textSize,"Select Creature","Select Creature",(255,255,255),(0,0,0),(position[0]+size[0]*0.5,(position[1]+size[1]*0.5)+size[1]*(i+1)),self.multiButtons[0])

        # buttons that can be activated
        self.multiButtons.append(ButtonGroup())
        Button((size[0]*0.5,size[1]),textSize,"Next","Next",(255,255,255),(0,0,0),(position[0]+size[0]*0.75,(position[1]+size[1]/2)+size[1]*(i+2)),self.multiButtons[1])
        self.multiButtons.append(ButtonGroup())
        Button((size[0]*0.5,size[1]),textSize,"Prev","Prev",(255,255,255),(0,0,0),(position[0]+size[0]*0.25,(position[1]+size[1]/2)+size[1]*(i+2)),self.multiButtons[2])


    def update(self, mousePos: tuple[int,int], mClick: bool) -> float:
    
        pressed = self.multiButtons[0].update(mousePos,mClick)
        if "Select Creature" in pressed:
            newName = FileFinder("Creatures",False)
            if newName:
                newName = newName["Name"]
                if newName not in self.nameDic:
                    self.nameDic[newName] = 0
                    self.updateButtons()
        else:
            for i in pressed:
                if i != None:
                    if len(self.buttonList[self.page]) >= i+1:
                        name = self.buttonList[self.page][i][0]
                        self.nameDic.pop(name)
                        self.updateButtons()

        pressed = self.multiNumB.update(mousePos,mClick)
        for i in pressed:
            if i != None:
                if len(self.buttonList[self.page]) >= i+1:
                    num = NumEditor()
                    name = self.buttonList[self.page][i][0]
                    self.nameDic[name] = num
                    self.updateButtons()
                else:
                    message("Error No Creature Set")
        
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
        for name in self.nameDic:
            if len(self.buttonList[-1]) < self.quantity:
                self.buttonList[-1].append([name,self.nameDic[name]])
            else:
                self.buttonList.append([[name,self.nameDic[name]]])
        buttonText = {}
        numText = {}
        if len(self.buttonList[self.page]) == 0:
            i = -1
        else:
            for i in range(len(self.buttonList[self.page])):
                buttonText[i] = self.buttonList[self.page][i][0]
                numText[i] = str(self.buttonList[self.page][i][1])
        for j in range(i+1 ,self.quantity):
            buttonText[j] = ""
            numText[j] = ""
        self.amountOfPages = len(self.buttonList)-1
        # change the button text to match

        self.multiButtons[0].setText(buttonText)
        self.multiNumB.setText(numText)




    def draw(self, screen: pg.Surface) -> None:
        # display the button then text
        self.multiButtons[0].draw(screen)
        if len(self.buttonList)-1 > self.page:
            pressed = self.multiButtons[1].draw(screen)
        
        elif self.page > 0:
            pressed = self.multiButtons[2].draw(screen)

        self.multiNumB.draw(screen)
    
    def getValue(self) -> tuple[str, int]:
        return self.name, self.nameDic
    
    def setValue(self, data: dict) -> None:
        self.nameDic = data[self.name]
        self.updateButtons()