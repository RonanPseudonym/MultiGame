import socketio, pyno, ansi, time, os

socket = socketio.Client()
messages = []

global typing
typing = []

global inp, name, color
inp = ""
name = ""
color = ""

width, height = 40, 20

grid = []

for i in range(height):
    row = []
    for j in range(width):
        row.append("░")
    grid.append(list(row))

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
    os.system("clear")
    messages.append(formatTyping(typing))
    messages.append("")
    messages.append(inp)
    for i in range(len(grid)): 
        try: print("".join(grid[i])+" "+messages[i])
        except: print("".join(grid[i]))
    del messages[-1]
    del messages[-1]
    del messages[-1]

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
    elif message[0] == "location": grid[message[1][0][1]][message[1][0][0]] = ansi.bg+message[1][1][1]+" "+ansi.esc
    elif message[0] == "not location": grid[message[1][1]][message[1][0]] = "░"
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