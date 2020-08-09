import socketio, time, pyno, ansi, os

global messages, latency
messages = []
latency = 0

print("Connecting...")

socket = socketio.Client()
socket.connect("ws://Black-Sun.ronanpseudonym.repl.co")

print("Connected")

# plt.plot(datapoints)
# plt.title("Latency")
# plt.show(block=False)
# plt.pause(1)
# plt.close('all')

socket.emit("push", "Pinging server @"+str(time.time()*1000000))

@socket.event
def recvMessage(message, sid):
    messages.append(message)
    if "Pinging server @" in message:
        oldTime = float(message.replace("Pinging server @",""))
        newTime = time.time()*1000000
        latency = int(int((newTime - oldTime)))
        # datapoints.append(latency)
        # plt.plot(datapoints)
        # plt.show(block=False)
        # plt.pause(1)
        # plt.close('all')
        time.sleep(10)
        socket.emit("push", "Pinging server @"+str(time.time()*1000000))
    os.system("clear")
    try: 
        print("\n".join(messages)+"\n\nLatency: "+ansi.color+"3m"+str(latency)+" microseconds"+ansi.esc+" ["+str(latency/1000000)+" seconds] "+ansi.hidecursor)
        if latency > 1000000: pyno.notify("Latency warning","Latency "+str(latency),"Horn")
    except: pass

while True:
    if len(messages) > 100: del messages[0]

# pyno.notify("An error ocurred","DowntimeBot was unable to complete the specified task","Horn")