import pygame as pg
import sys, time, os, json
from settings import SCALE, FPS, screen

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

def SaveFile(name: str, type: str, dictionary: dict) -> None:
    fileSaved = False
    file = f"assets/{type}/{name}.json"
    
    if os.path.exists(file):
        # the file exists, asking user if they want to overwrite the data
        if Confirm("Overwrite","This file already exists"):
            # overwriting file
            with open(file, "w+") as file:
                file.write(json.dumps(dictionary,indent=4))
            fileSaved = True
    else:
        # The file does no exist so it is safe to save the data
        with open(file, "w+") as file:
            file.write(json.dumps(dictionary,indent=4))
        fileSaved = True

    
    if fileSaved:
        # display message that file has been saved
        message(f"File saved as {name}")
    else:
        # display message that file has not been saved
        message("File has not been saved")

def LoadFile(name: str, type: str, messageOn: bool=True) -> dict:
    try:
        # try to open file
        with open(f"assets/{type}/{name}.json","r") as file:
            data = json.load(file)
        data['Name'] = name 
    except:
        # no file at location will cause an error
        message(f"File {name}.json could not be found")
        return None
    print
    # file loaded message
    if messageOn:
        message(f"File {name} loaded")
    return data

def folderRead(folder: str) -> list:
    names = [[]]
    files = os.listdir(folder)
    files.sort()
    for file in files:
        if len(names[len(names)-1]) < 12:
            names[len(names)-1].append(file.removesuffix(".json"))
        else:
            names.append([])
            names[len(names)-1].append(file.removesuffix(".json"))
    return names

def deleteFile(folder: str, name: str) -> None:
    try:
        open(f"assets/{folder}/{name}.json","r")
        os.remove(f"assets/{folder}/{name}.json")
    except:
        message("File could not be deleted")

def message(text: str, length: int=800, timeDelay: int=1) -> None:
    SpriteRender((length,50),(255,255,255),(800,450),screen)
    TextRender(text,2,(0,0,0),(800,450),screen)
    pg.display.flip()
    time.sleep(timeDelay) 
