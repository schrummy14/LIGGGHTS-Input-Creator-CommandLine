#!/usr/bin/python3

from options import Options as Opt
from helpers import clear
def main():
    opts = Opt()
    clear()
    opts.printOptions()
    

if __name__ == "__main__":
    main()