import pygame as pg
import sys,time
from baseSprites import confirmButtons, confirmDefault,textEditorButtons
from settings import FPS, screen, LETTERS
from functions import SpriteRender, TextRender

def NumEditor(number: int=0) -> int:
    print("Num Editor")
    if number == 0:
        numbers = ""
    else:
        numbers = str(number)
    
    while True:
        mClick = False
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                elif event.key == pg.K_KP_ENTER or event.key == pg.K_RETURN:
                    return int(numbers)
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
                    return int(numbers)
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

def TextEditor(text: str="", message: str="", allowNumbers: bool=True) -> str:
    print("Text Editor")

    while True:
        mClick = False
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                elif event.key == pg.K_KP_ENTER or event.key == pg.K_RETURN:
                    return text
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

                elif event.key >= 48 and event.key <=57:
                    letter = event.key - 48
                    # add number to the string
                    text += str(letter)
                    # check for to many numbers
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
        TextRender(message,2,(255,255,255),(800,300),screen)

        pg.display.flip()
        # run at 60 fps
        time.sleep(1/ FPS)
