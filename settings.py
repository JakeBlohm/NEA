import pyautogui
import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
print(pyautogui.size())
SCALE = SCREEN_WIDTH / 1600
print(SCALE)
FPS = 60
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

print("Seting Up")
# General setup
pg.init()
screen = pg.display.set_mode((0,0),pg.FULLSCREEN, display=0)
pg.display.set_caption("NEA")
clock = pg.time.Clock()