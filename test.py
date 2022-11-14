import pygame as pg
import random

bearing = random.randint(0,360)
vector = pg.math.Vector2(1,0).rotate(bearing)
print(vector)
vector.rotate_ip(random.randint(0,360))
print(vector)