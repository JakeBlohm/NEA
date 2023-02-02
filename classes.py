import pygame as pg
from settings import SCALE
from baseFunctions import TextEditor, NumEditor

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


class TextBox(pg.sprite.Sprite):
    def __init__(self, size: tuple[int,int], 
                textSize: tuple[int,int], startValue: str, 
                name: str, valueType: str,
                colour: tuple[int,int,int], textColour: tuple[int,int,int], 
                pos: tuple[int,int], group, 
                deleteValueOnClick: bool=False) -> None:

        print("Creating TextBox")
        # Create TextBox
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([size[0]*SCALE, size[1]*SCALE])
        self.image.fill(colour)
        self.rect = self.image.get_rect(center = (pos[0]*SCALE,pos[1]*SCALE))
        
        self.value = startValue
        self.font = pg.font.SysFont('Arial', int(24*SCALE*textSize))
        self.text = self.font.render(str(startValue), 0, pg.Color(textColour))

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
                    self.text = self.font.render(str(value), 0, pg.Color(self.textColour))

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
            self.text = self.font.render(str(self.value), 0, pg.Color(self.textColour))