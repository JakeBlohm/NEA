import threading,time,random,math
import pygame as pg


positions = []
for i in range(1,1000):
    positions.append((random.randint(1,1000),random.randint(1,1000)))

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

c=0
start_time = time.perf_counter()

for p1 in positions:
    for p2 in positions:
        if distance(p1, p2) <= 10:
            c+=1

finish_time = time.perf_counter()

print(f"it took {finish_time - start_time}s")
print(c)




c=0
start_time = time.perf_counter()

for position in positions:
    high = [position[0] + 10, position[1] + 10]
    low = [position[0] - 10, position[1] - 10]
    for target in positions:
        if low[0] < target[0] < high[0] and low[1] < target[1] < high[1]:
            targetVector = pg.math.Vector2(target[0] - position[0],target[1] - position[1])
            distances = targetVector.magnitude()
            if distances <= 10:
                c+=1


finish_time = time.perf_counter()

print(f"it took {finish_time - start_time}s")
print(c)