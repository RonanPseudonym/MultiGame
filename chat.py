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
        break
    except:
        print("Waking server...")
        time.sleep(10)

typing = False

x, y = 0, 0

try: 
    wsm.push(["location",[[x,y],[hostname, color]]])
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
                if not y - 1 == -1:
                    wsm.push(["not location",[x,y]])
                    y -= 1
                    wsm.push(["location",[[x,y],[hostname, color]]])
            elif key == "down": 
                if not y + 1 == height:
                    wsm.push(["not location",[x,y]])
                    y += 1
                    wsm.push(["location",[[x,y],[hostname, color]]])
            elif key == "left": 
                if not x - 1 == -1:
                    wsm.push(["not location",[x,y]])
                    x -= 1
                    wsm.push(["location",[[x,y],[hostname, color]]])
            elif key == "right": 
                if not x + 1 == width:
                    wsm.push(["not location",[x,y]])
                    x += 1
                    wsm.push(["location",[[x,y],[hostname, color]]])
            else: 
                inp.append(key)
                typing = True
            wsm.passInp("".join(inp)+"▉")
            os.system("clear")
            wsm.drawScreen(wsm.passTypers(), "".join(inp)+"▉")
            if oldTyping != typing:
                oldTyping = typing
                wsm.push(["typing status",[hostname,typing]])
        wsm.push(["typing status",[hostname,False]])
        del inp[0]
        inp = parse.parse(inp, color)
        if "".join(inp) == "/exit": 
            wsm.disconnect(hostname)
            quit()
        elif len(inp) > 0: wsm.push(["chat",[color, hostname, "".join(inp)]])

except KeyboardInterrupt: wsm.disconnect(hostname)