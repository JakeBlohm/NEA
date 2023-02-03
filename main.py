import sys
import time
import pygame as pg
import simulation
from sprites import (
    menuButtons, creatureCreatorButtons, creatureCreatorBox,
    creatureCreatorDefault, environmentCreatorBox, environmentCreatorButtons,
    environmentCreatorDefault, simulationCreatorBox, simulationCreatorButtons,
    simulationCreatorDefault
    )
from settings import FPS, screen,clock
from functions import SaveFile, deleteFile, LoadFile
from baseFunctions import Confirm
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

                    # screen,[[Quantity,CreatureDict]],[[foods suff],[drains]],[aumount, value, persec]
                    sim = simulation.Simulation(screen,creatures,[[100,50,20],[0.01,0.01,0.001,0.001]])
                    print(creatures)
                    simData = sim.run()

                    SaveFile(simulationCreatorBox.getValues()["Name"],"SimResults",simData)

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


# Menu Settup
running = True
while running:
    menu()
    print("???")
    clock.tick()
    pg.display.flip()