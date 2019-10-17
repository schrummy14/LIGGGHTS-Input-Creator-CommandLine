from os import system, name

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def getNum(curStr):
    while True:
        val = input(curStr)
        try:
            val = float(val)
            break
        except ValueError:
            print(val + "is not a number.")
    return val

def print2screenOptions(curStr, isDone):
    if isDone:
        curStr += " | Done"
    print(curStr)