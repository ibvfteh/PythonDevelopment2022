from time import strftime
from pyfiglet import Figlet

def date(format="%Y %d %b, %A", font="graceful"):
    figlet = Figlet(font=font)
    return figlet.renderText(strftime(format))
