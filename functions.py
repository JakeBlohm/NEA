import pygame as pg
import sys, time, os, json
from settings import SCALE, FPS, screen
from baseSprites import confirmButtons, confirmDefault

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
                elif event.key == pg.K_KP_ENTER or event.key == pg.K_RETURN:
                    return True
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

def SaveFile(name: str, type: str, dictionary: dict) -> bool:
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
        return True
    else:
        # display message that file has not been saved
        message("File has not been saved")
        return False

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

def line(pointOne,pointTwo,location,scale,colour=(0,0,0)):
    pg.draw.line(screen,colour,(location[0]+pointOne[0]*scale[0],location[1]+pointOne[1]*scale[1]),(location[0]+pointTwo[0]*scale[0],location[1]+pointTwo[1]*scale[1]),int(2*SCALE))

def graphs(data,scalers,animalNum,dataName,location,scale,colour=(255,0,0),lineColour = (0,0,0)):
    location = (location[0]*SCALE,location[1]*SCALE)
    scale = (scale[0]*SCALE,scale[1]*SCALE)
    line((-100,100),(-100,-100),location,scale,lineColour)
    line((-100,100),(100,100),location,scale,lineColour)

    for i in range(-100, 101, 50):
        line((-100, i), (-101, i), location, scale, lineColour)

    TextRender(dataName,1,lineColour,((location[0]/SCALE),(location[1]/SCALE)-80*scale[1]),screen)
    values = data[dataName][animalNum]
    maxCycle = len(values) 
    valueScale = scalers[dataName]
    cycleScale = 200/(maxCycle-1)
    tempValue1 = 100-(values[0]*valueScale)

    print(str(int(valueScale*200)))

    for i, value in enumerate([200 / valueScale, (200 / valueScale / 4) * 3, 200 / valueScale / 2, 200 / valueScale / 4]):
        TextRender(str(int(value)), 0.5, lineColour, ((location[0] / SCALE) - 65 * (scale[0]+0.2), (location[1] / SCALE) + (-60 + i * 30) * scale[1]), screen)

    TextRender("0",0.5,lineColour,((location[0]/SCALE)-65*(scale[0]+0.2),(location[1]/SCALE)+60*scale[1]),screen)

    for i in range(maxCycle-1):
        tempValue2 = 100-(values[i+1]*valueScale)

        line((((i)*cycleScale)-100,tempValue1),(((i+1)*cycleScale)-100,tempValue2),location,scale,colour)

        tempValue1 = tempValue2

def dataConverter(data,dataTypes,animalsNames):
    newData = {}
    dataScales = {}
    for dataName in dataTypes:
        animalsData = []
        allValues = []
        for animalName in animalsNames:
            values = []
            for cycle in data:
                value = data[cycle][animalName][dataName]
                values.append(value)
                allValues.append(value)
            animalsData.append(values)
        newData[dataName] = animalsData
        dataScales[dataName] = 200/max(allValues)
    return newData, dataScales

def stringToRgb(input_string):
    # Hash the input string to a 32-bit integer
    hash_value = hash(input_string) & 0xffffffff
    # Convert the 32-bit integer to 3 8-bit integers representing R, G, and B
    r = (hash_value >> 16) & 0xff
    g = (hash_value >> 8) & 0xff
    b = hash_value & 0xff
    return (r, g, b)