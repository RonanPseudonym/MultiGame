from PIL import Image
import os

fname = input("> ")

image = Image.open(os.path.dirname(os.path.realpath(__file__))+"/"+fname+".png")

possibilities = {
    (255, 255, 255, 255): "0",
    (0, 0, 0, 255):       "2",
    (0, 15, 255, 255):    "1",
    (255, 0, 0, 255):     "^",
    (0, 128, 128, 255):   "w"
}

base = list(image.getdata())
grid, tp = [], []

for i in range(20):
    row = []
    for j in range(20):
        row.append(base[(i*20)+j])
    grid.append(list(row))

for i in range(len(grid)):
    row = []
    for j in range(len(grid[i])):
        if grid[i][j] in possibilities: 
            for _ in range(0, 2): row.append(possibilities.get(grid[i][j]))
        else: 
            for _ in range(0, 2): row.append("")
    tp.append("".join(row))

f = open(os.path.dirname(os.path.realpath(__file__))+"/"+fname+".txt","w+")
f.write("\n".join(tp))
f.close()