#!/usr/bin/python3
from options import Options as Opt
from helpers import clear
def main():
    clear()
    opts = Opt()
    opts.printOptions()
    
if __name__ == "__main__":
    main()
""" 
Add many sanity checks...
In Contact model, force order or check???
Add more sanity checks to Young's modulus values.... you know, 1.0e9 or about...
Poisson's ratios must be between 0 and 0.5
Force COR to be between 0 and 1
Force COF to be between 0 and 1
"""
