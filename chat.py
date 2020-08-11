print("Starting up...")

import wsm, ansi, time, getch, os, random, styles, parse

hostname = input("Enter name: ").strip().replace(" ","-").replace("_","-").replace("@","").replace("*","").replace("`","").lower()
color = str(random.randint(1, 230))+"m"

inp = ["> "]

wsm.passName(hostname)

wsm.passColor(color)

wsm.passInp("".join(inp))

width, height = 40, 20

print("Connecting...")

while True:
    try: 
        wsm.connect("ws://Black-Sun.ronanpseudonym.repl.co", hostname)
        print("Connected")
        break
    except:
        print("Waking server... (please wait about thirty seconds) ")
        time.sleep(30)

typing = False

x, y, gridx, gridy = 20, 0, 0, 0

grid = []

directory = os.path.dirname(os.path.realpath(__file__))

def tile(x, y):
    grid = []

    f = open(directory+"/"+str(gridx)+"_"+str(gridy)+".txt")

    for line in f: 
        grid.append(list(line.replace("\n","")))

    wsm.passGrid(grid, x, y)

    return grid

try: 
    grid = tile(gridx, gridy)
    wsm.push(["location",[[[x,y],[gridx,gridy]],[hostname, color]]])
    while True:
        inp = ["> "]
        while True: 
            oldTyping = typing
            key = getch.getch()
            if key == "\n": 
                wsm.passInp("> ▉")
                typingStatus = False
                break
            elif key == "backspace": 
                if len(inp) > 2: del inp[-1]
                elif len(inp) <= 2:
                    typing = False
                    if len(inp) == 2: del inp[-1]
            elif key == "up":
                if y <= 0: 
                    wsm.push(["not location",[[x,y],[gridx,gridy]]])
                    gridy += 1
                    y = height-1
                    grid = tile(gridx, gridy)
                    wsm.push(["location",[[[x,y],[gridx,gridy]],[hostname, color]]])
                    break
                elif grid[y-1][x] == "0":
                    wsm.push(["not location",[[x,y],[gridx,gridy]]])
                    y -= 1
                    wsm.push(["location",[[[x,y],[gridx,gridy]],[hostname, color]]])
            elif key == "down":
                if y >= height-1: 
                    wsm.push(["not location",[[x,y],[gridx,gridy]]])
                    gridy -= 1
                    y = 0
                    grid = tile(gridx, gridy)
                    wsm.push(["location",[[[x,y],[gridx,gridy]],[hostname, color]]])
                    break 
                elif grid[y+1][x] == "0":
                    wsm.push(["not location",[[x,y],[gridx,gridy]]])
                    y += 1
                    wsm.push(["location",[[[x,y],[gridx,gridy]],[hostname, color]]])
            elif key == "left":
                if x >= width-2: 
                    wsm.push(["not location",[[x,y],[gridx,gridy]]])
                    gridx += 1
                    x = 0
                    grid = tile(gridx, gridy)
                    wsm.push(["location",[[[x,y],[gridx,gridy]],[hostname, color]]])
                    break
                elif grid[y][x-1] == "0":
                    wsm.push(["not location",[[x,y],[gridx,gridy]]])
                    x -= 1
                    wsm.push(["location",[[[x,y],[gridx,gridy]],[hostname, color]]])
            elif key == "right": 
                if x <= 1: 
                    gridx -= 1
                    x = width-1
                    grid = tile(gridx, gridy)
                    break
                elif grid[y][x+1] == "0":
                    wsm.push(["not location",[[x,y],[gridx,gridy]]])
                    x += 1
                    wsm.push(["location",[[[x,y],[gridx,gridy]],[hostname, color]]])
            else: 
                inp.append(key)
                typing = True
            if oldTyping != typing:
                oldTyping = typing
                wsm.push(["typing status",[hostname,typing]])
            wsm.passInp("".join(inp)+"▉")
            wsm.drawScreen(wsm.passTypers(), "".join(inp)+"▉")
        typing = False
        wsm.push(["typing status",[hostname,typing]])
        del inp[0]
        inp = parse.parse(inp, color)
        if "".join(inp) == "/exit": 
            wsm.disconnect(hostname)
            quit()
        elif len(inp) > 0: wsm.push(["chat",[color, hostname, "".join(inp)]])

except KeyboardInterrupt: wsm.disconnect(hostname)