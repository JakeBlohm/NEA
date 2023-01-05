positions = []
for i in range(0,2):
    for j in range(0,2):
        positions.append((i,j))


for i, p1 in enumerate(positions):
    for p2 in positions[i+1:]:
        print(p1,p2)