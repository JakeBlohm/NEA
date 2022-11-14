import os
names = [[]]
files = os.listdir("Assets/Creatures")
for file in files:
    if len(names[len(names)-1]) < 6:
        names[len(names)-1].append(file[:-4])
    else:
        names.append([])
        names[len(names)-1].append(file[:-4])
print(names)