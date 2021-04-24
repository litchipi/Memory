
import sys

COLORS = {
        "white":"99",
        "red":"91",
        "yellow":"93",
        "blue":"94",
        }

EFFECTS = {
        "normal":"0",
        "bold":"1",
        "italic":"3",
        }

RESET = "\033[0m"

def create_style(color="white", effect="normal"):
    return "\033[{};{}m".format(EFFECTS[effect], COLORS[color])

def error(msg, help_msg=None):
    print(create_style("red", "bold") + "! Error ! " + RESET + create_style("white", "bold") + str(msg) + RESET)
    if help_msg:
        print("")
        print(help_msg)
        print("")
    sys.exit(1);

def warning(msg):
    print(create_style("yellow", "bold") + "/!\ Warning " + RESET + str(msg))

def progress(msg, color="blue", heading=None):
    s = ""
    if heading:
        s = create_style(color, "bold") + str(heading) + "> " + RESET
    else:
        s = create_style(color) + "--- " + RESET
    s += create_style(color) + str(msg) + RESET
    print(s)
