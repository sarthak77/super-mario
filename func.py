#contains imp functions

def checkmv(charac):
    a=["|","@","x"]
    if charac in a:
        return(0)
    else:
        return(1)


def checkrv(charac1,charac2):
    if charac1=="~" and charac2=="~":
        return(-1)
    else:
        return(0)

#tells which objects to climb on
def checkj(charac1,charac2):
    a=["|","@","O","M","Q","?","C","$","P"]
    if charac1 in a or charac2 in a:
        return(-1)
    else:
        return(0)