import termios, sys

stdin_fd = sys.stdin.fileno()

substitutions = {
    "\x7f": "backspace",
    "        ": "tab"
}

chsubs = {
    "A": "up",
    "B": "down",
    "C": "right",
    "D": "left",

}

def getch():

    new = termios.tcgetattr(stdin_fd)
    new[3] = new[3] & ~termios.ICANON
    new[3] = new[3] & ~termios.ECHO

    try:
        termios.tcsetattr(stdin_fd, termios.TCSADRAIN, new)

        ch = sys.stdin.read(1)
        if ch in substitutions: return substitutions[ch]

        if ch != '\x1b': return ch

        ch = sys.stdin.read(1)
        if ch != '[': return ch

        ch = sys.stdin.read(1)

        if ch in chsubs: ch = chsubs.get(ch)
        return ch

    except: return 'exception'

if __name__ == "__main__":
    while True:
        print(getch())
