import ansi, styles

def parse(inp, color):
    closeBold = False
    closeItalic = False
    closeMono = False
    for i in range(0, len(inp)):
        if inp[i] == "@":
            inp[i] = ansi.color+"3m"+inp[i]
        elif inp[i] == " ":
            inp[i] = ansi.color+color+inp[i]
        elif inp[i] == "*":
            closeBold = not closeBold
            if closeBold == True: inp[i] = ansi.bold
            else: inp[i] = ansi.esc+ansi.color+color
        elif inp[i] == "_":
            closeItalic = not closeItalic
            inp[i] = ""
        elif inp[i] == "`":
            closeMono = not closeMono
            inp[i] = ""
        elif closeItalic == True:
            if inp[i] in list(styles.normal): inp[i] = str(styles.italic[list(styles.normal).index(inp[i])])
        elif closeMono == True:
            if inp[i] in list(styles.normal): inp[i] = str(styles.mono[list(styles.normal).index(inp[i])])
    return inp
