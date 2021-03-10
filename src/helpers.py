"""
Helper functions for the rest of the program
"""
from os import system, name, path, sep
from tkinter import Tk
from tkinter import filedialog as fd

import glob
import numpy as np

## Boolian variable to determine if a screen is present
noTk = False
try:
    Tk().withdraw()
except:
    print("Could not find display...")
    print("Using pure command line")
    noTk = True

global primeNumbers
## Prime number list to make sure each prime number is unique
primeNumbers = []

## Clears the terminal screen
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

## Returns a boolean to check yes/no
#
#  @param curStr The string the user sees that contains the yes/no question
def getYesNo(curStr):
    while True:
        val = input(curStr)
        if val in ['yes','no']:
            break
        else:
            print("You must eneter 'yes' or 'no'")
    return val

## Returns number given a question
#
#  @param curStr The string the users sees that contains the value question
def getNum(curStr):
    while True:
        val = input(curStr)
        try:
            val = float(val)
            break
        except ValueError:
            print(val + "is not a number.")
    return val

## Returns a new prime number that has not been used before
def getNewPrime():
    global primeNumbers
    kStart = 20600
    kEnd = 1000*kStart
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

## Checks if a number is prime
#
#  @param p An integer that could be prime
def isPrime(p):
    if p%2 == 0 and p > 2:
        return False
    notPrime = False
    for k in range(3,int(np.sqrt(p)),2):
        if p % k == 0:
            notPrime = True
            break
    return not notPrime

## Returns a potentially modified string
#
#  @param curStr The string that could be modified
#  @param isDone A boolean value to determine if the string should be modified
def print2screenOptions(curStr, isDone):
    if isDone:
        curStr += " | Done"
    print(curStr)

## Returns the full file path contained in a list
#
#  @param str_array The array containing the file path parts
def fullfile(str_array):
    curStr = ''
    for k in str_array:
        curStr += k + sep
    return curStr[:-1]

## Asks the user to provide a file
#
#  @param fType The file type that needs to be returned
#  @param msg2user The message provided to the user
def getFileName(fType, msg2user):
    if noTk:
        while True:
            right_file = True
            file_name = input(msg2user + ' ')
            print(file_name)

            if len(file_name) < 4:
                right_file &= False
                file_type = None
            else:
                split_str = file_name.split('.')
                file_type = split_str[-1]

            print(file_type)

            if not file_type in fType and file_type != 'ANY_TYPE':
                right_file &= False

            if path.exists(file_name) and right_file:
                break

            print("Not a valid option...")
            print("Valid files at location with filetype: %s"%(file_type))
            file_directory = file_name.split(sep)
            file_directory[-1] = '*.'+file_type
            print(fullfile(file_directory))
            all_files = glob.glob(fullfile(file_directory))
            for cur_file in all_files:
                print(cur_file)
    else:
        file_name = fd.askopenfilename()
    return file_name
