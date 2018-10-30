"""
COLORS ADDED IN THIS MODULE
"""
COLORS = {
    'Black': '\x1b[1;30m',
    'Blue': '\x1b[1;94m',
    'Green': '\x1b[1;92m',
    'Cyan': '\x1b[0;36m',
    'Red': '\x1b[0;31m',
    'Purple': '\x1b[0;35m',
    'Brown': '\x1b[0;33m',
    'Gray': '\x1b[0;37m',
    'Dark Gray': '\x1b[1;30m',
    'Light Blue': '\x1b[1;34m',
    'Light Cyan': '\x1b[1;36m',
    'Light Red': '\x1b[1;31m',
    'Light Purple': '\x1b[1;35m',
    'Yellow': '\x1b[1;33m',
    'White': '\x1b[1;37m'
}


def getcolor(charac):
    """
    COLORS BASED ON CHARACTER ADDED HERE
    """

    if charac in ["^", "M", "*", "+"]:
        color = "White"
    elif charac in ["#", "@"]:
        color = "Brown"
    elif charac == "-":
        color = "Blue"
    elif charac == "/":
        color = "Green"
    elif charac == "|":
        color = "Green"
    elif charac in ["?", "P", "C", "$"]:
        color = "Brown"
    elif charac == "O":
        color = "Yellow"
    elif charac in ["Q", "x"]:
        color = "Red"
    elif charac == "~":
        color = "Cyan"
    elif charac == "H":
        color = "Yellow"
    elif charac == ".":
        color = "Black"

    else:
        color = "Red"

    return COLORS[color]+charac+'\x1b[0m'
