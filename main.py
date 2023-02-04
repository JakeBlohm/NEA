import sys
import time
import pygame as pg
import simulation
from sprites import (
    menuButtons, creatureCreatorButtons, creatureCreatorBox,
    creatureCreatorDefault, environmentCreatorBox, environmentCreatorButtons,
    environmentCreatorDefault, simulationCreatorBox, simulationCreatorButtons,
    simulationCreatorDefault, GraphDisplayButtons
    )
from settings import FPS, screen,clock
from baseFunctions import TextEditor
from functions import SaveFile, deleteFile, LoadFile,Confirm, dataConverter, graphs, stringToRgb
from advFunctions import FileFinder

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

                elif press == "Display Data":
                    DisplayData()
                

        # clear screen and set background colour
        screen.fill((0,0,0))
        # display the buttons
        menuButtons.draw(screen)

        pg.display.flip()
        
        # run menu at set fps
        time.sleep(1/ FPS)
    
def CreatureCreator() -> None:
    print("Creature Creator")
    run = True
    while run:
        mClick = False
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
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
    run = True
    while run:
        mClick = False
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
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
    run = True
    while run:
        mClick = False
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
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
                    DictCreatures = simulationCreatorBox.getValues()["Creatures"]
                    creatures = []

                    for creature in DictCreatures:
                        quantity = DictCreatures[creature]
                        values = LoadFile(creature,"Creatures",False)
                        creatures.append([quantity,values])

                    # screen,[[Quantity,CreatureDict]],[[foods suff],[drains]],[amount, value, persec]
                    sim = simulation.Simulation(screen,creatures,[[100,50,20],[0.01,0.01,0.001,0.001]])
                    print(creatures)
                    simData = sim.run()
                    while True:
                        simName = TextEditor(simulationCreatorBox.getValues()["Name"],"Save data as")
                        if simName:
                            if SaveFile(simName,"SimResults",simData):
                                break
                        else:
                            break
                    DisplayData(simData)

                elif press == "Save":
                    data = simulationCreatorBox.getValues()
                    print(data)
                    name = data.pop("Name")
                    SaveFile(name,"Simulations",data)
                elif press == "Load":
                    data = FileFinder("Simulations")
                    if data:
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

def DisplayData(data = None) -> None:
    print("Display Data")
    run = True
    if data:
        names= []
        dataTypes = []
        animalColours = []
        for name in data[0]:
            names.append(name)
            animalColours.append(stringToRgb(name))
        for type in data[0][name]:
            dataTypes.append(type)
        newData,scalers = dataConverter(data,dataTypes,names)

    while run:
        mClick = False
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mClick = True

        
        mousePos=pg.mouse.get_pos()

        pressed = GraphDisplayButtons.update(mousePos, mClick) 

        # Detecting if there was a button pressed
        for press in pressed:
            if press != None:
                # Find what button was pressed
                if press == "Exit":
                    return
                elif press == "Load":
                    data = FileFinder("SimResults")
                    data.pop("Name")
                    names= []
                    dataTypes = []
                    animalColours = []
                    for name in data["0"]:
                        names.append(name)
                        animalColours.append(stringToRgb(name))
                    for type in data["0"][name]:
                        dataTypes.append(type)
                    newData,scalers = dataConverter(data,dataTypes,names)

        # clear screen and set background colour
        screen.fill((0,0,0))
        # display the buttons

        GraphDisplayButtons.draw(screen)

        if data:
            for animalNum in range(len(names)):
                for i in range(5):
                    graphs(newData,scalers,animalNum,dataTypes[i],(800,160*i + 100),(7,0.6),animalColours[animalNum],(255,255,255))

        pg.display.flip()

        # run at set fps
        time.sleep(1/ FPS)


# Menu Settup
running = True
while running:
    menu()
    print("???")
    clock.tick()
    pg.display.flip()