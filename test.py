data= {100:[{"speed":10,"fov":30}],200:[{"speed":11,"fov":31}]}
animal = 0
stat = "speed"
for cycle in data:
    print(data[cycle][animal][stat])