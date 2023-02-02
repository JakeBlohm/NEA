import sys, time
import pygame as pg
from medSprites import fileFinderButtons, fileFinderBox
from functions import folderRead, LoadFile
from settings import screen, FPS

def FileFinder(valueType: str, messageOn:bool = True) -> dict:
    print("File Finder")
    # Get names for buttons
    fileNames = folderRead(f"assets/{valueType}")
    page = 0
    # convert the names from a list to a dict
    buttonText = {}
    for i in range(len(fileNames[page])):
        buttonText[i] = fileNames[page][i]
    for j in range(i+1 ,12):
        buttonText[j] = ""
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
                        data = LoadFile(name,valueType, messageOn)
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
                    data = LoadFile(name,valueType, messageOn)
                    if data:
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
