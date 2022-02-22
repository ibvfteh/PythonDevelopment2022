from time import strftime
from pyfiglet import Figlet

def date(format="%Y %d %b, %A", font="graceful"):
    figlet = Figlet(font=font)
    print(figlet.renderText(strftime(format)))
