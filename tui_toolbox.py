
import sys

COLORS = {
        "white":"99",
        "red":"91",
        }

EFFECTS = {
        "normal":"0",
        "bold":"1",
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
