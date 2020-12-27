import glob
import numpy as np
from os import system, name, path, sep
from tkinter import Tk
from tkinter import filedialog as fd

noTk = False
try:
    Tk().withdraw()
except:
    print("Could not find display...")
    print("Using pure command line")
    noTk = True

global primeNumbers
primeNumbers = []

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def getYesNo(curStr):
    while True:
        val = input(curStr)
        if val in ['yes','no']:
            break
        else:
            print("You must eneter 'yes' or 'no'")
    return val

def getNum(curStr):
    while True:
        val = input(curStr)
        try:
            val = float(val)
            break
        except ValueError:
            print(val + "is not a number.")
    return val

def getNewPrime():
    global primeNumbers
    kStart = 20600
    kEnd = 1000000*kStart
    while True:
        k = np.random.randint(kStart,kEnd)
        p1 = 6*k-1
        p2 = 6*k+1
        if isPrime(p1):
            if not p1 in primeNumbers:
                primeNumbers.append(p1)
                return p1
        if isPrime(p2):
            if not p2 in primeNumbers:
                primeNumbers.append(p2)
                return p2

def isPrime(p):
    if p%2 == 0 and p > 2:
        return False
    notPrime = False
    for k in range(3,int(np.sqrt(p)),2):
        if p % k == 0:
            notPrime = True
            break
    return not notPrime


def print2screenOptions(curStr, isDone):
    if isDone:
        curStr += " | Done"
    print(curStr)

def fullfile(str_array):
    curStr = ''
    for k in str_array:
        curStr += k + sep
    return curStr[:-1]


def getFileName(fType, msg2user):
    if noTk:
        while True:
            rightFile = True
            fileName = input(msg2user + ' ')
            print(fileName)
            
            if len(fileName) < 4:
                rightFile &= False
                fileType = None
            else:
                split_str = fileName.split('.')
                fileType = split_str[-1]

            print(fileType)
            
            if not fileType in fType and fileType != 'ANY_TYPE':
                rightFile &= False
            
            if path.exists(fileName) and rightFile:
                break
            else:
                print("Not a valid option...")
                print("Valid files at location with filetype: %s"%(fileType))
                fileDirectory = fileName.split(sep)
                fileDirectory[-1] = '*.'+fileType
                print(fullfile(fileDirectory))
                allFiles = glob.glob(fullfile(fileDirectory))
                for curFile in allFiles:
                    print(curFile)
    else:
        fileName = fd.askopenfilename()
    return fileName
