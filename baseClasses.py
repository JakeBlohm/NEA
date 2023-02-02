
import pygame as pg
from settings import SCALE

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

