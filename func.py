"""
contains imp functions
"""


def checkmv(charac):
    """
    checks if can move forward or not
    """
    arr = ["|", "@", "x", "O"]
    if charac in arr:
        return 0
    return 1


def checkrv(charac1, charac2):
    """
    checks if river ahead
    """
    if charac1 == "~" and charac2 == "~":
        return -1
    return 0


def checkj(charac1, charac2):
    """
    tells which object to climb on
    """
    arr = ["|", "@", "O", "M", "Q", "?", "C", "$", "P"]
    if charac1 in arr or charac2 in arr:
        return -1
    return 0
