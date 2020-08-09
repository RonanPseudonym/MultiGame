import os, platform

def notify(title, content, sound):
    if platform.system() == "Darwin": os.system('''osascript -e 'display notification "'''+content+'''" with title "'''+title+'''" sound name "'''+sound+'''"'''+"'")
    else: os.system('notify-send "'+title+'" "'+content+'"')