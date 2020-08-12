import socketio, pyno, ansi, time, os

socket = socketio.Client()
messages = []

global typing, grid
typing, grid = [], []

global inp, name, color
inp = ""
name = ""
color = ""

global gridx, gridy, x, y

x = 0
y = 0

width, height, x, y = 40, 20, 0, 0

substitutions = {
    "2": ansi.color+"241m"+ansi.bg+"240m "+ansi.esc,
    "1": ansi.bg+"244m "+ansi.esc,
    "0": ansi.bg+"250m "+ansi.esc,
    "w": ansi.bg+"27m"+ansi.color+"69m "+ansi.esc
}

def formatGrid(grid):
    viewGrid = []
    for i in range(0, len(grid)):
        row = []
        for j in range(0, len(grid[i])): 
            if grid[i][j] in substitutions: row.append(substitutions.get(grid[i][j]))
            else: row.append(grid[i][j])
        viewGrid.append(list(row))
    return(viewGrid)

def push(message): socket.emit("push", message)

def connect(uri, name):
    socket.connect(uri)
    push(["join", name+" has joined the chat"])

def disconnect(name): push(name+" has left the chat")

def formatTyping(typing):
    if len(typing) == 0: return ""
    elif len(typing) == 1: return "".join(typing)+" is typing"
    else: return ", ".join(typing)+" are typing"

def drawScreen(typing, inp):
    messages.append(formatTyping(typing))
    messages.append("")
    messages.append(inp)
    viewGrid = formatGrid(grid)
    toPrint = []
    for i in range(len(grid)): 
        try: toPrint.append("".join(viewGrid[i])+" "+messages[i])
        except: toPrint.append("".join(viewGrid[i]))
    del messages[-1]
    del messages[-1]
    del messages[-1]
    os.system("clear")
    print("\n".join(toPrint))

def refresh():
    drawScreen(typing, inp)

@socket.event
def recvMessage(message, sid):
    if message[0] == "typing status":
        typer, status = message[1][0], message[1][1]
        if status == True: typing.append(typer)
        elif typer in typing: typing.remove(typer)
    elif message[0] == "chat":
        messages.append(message[1][1]+": "+ansi.color+message[1][0]+message[1][2]+ansi.esc)
        if len(messages) > height-3: del messages[0]
        if str("@"+name) in message[1][2]: pyno.notify(message[1][1]+" mentioned you",message[1][2].replace("[38;5;"+color,"").replace("[38;5;3m","").replace("[0m",""),"default")
    elif message[0] == "join":
        messages.append(message[1])
        pyno.notify(message[1],message[1],"default")
    elif message[0] == "location" and gridx == message[1][0][1][0] and gridy == message[1][0][1][1]: 
        grid[message[1][0][0][1]][message[1][0][0][0]] = ansi.bg+"250m"+ansi.color+message[1][1][1]+"●"+ansi.esc
        global x, y
        x, y = message[1][0][0][0],message[1][0][0][1]
    elif message[0] == "not location" and gridx == message[1][1][0] and gridy == message[1][1][1]: grid[message[1][0][1]][message[1][0][0]] = "0"
    elif message[0] == "location request" and gridx == message[1][0] and gridy == message[1][1] and name != message[1][2]: push(["location",[[[x,y],[gridx,gridy]],[name, color]]])
    drawScreen(typing, inp)

def passTypers():
    return typing

def getMessages(): return(messages)

def passInp(var):
    global inp
    inp = var

def passName(var):
    global name
    name = var

def passColor(var):
    global color
    color = var

def passGrid(a, b, c, d, e):
    global grid, gridx, gridy, x, y
    grid, gridx, gridy, x, y = a, b, c, d, e