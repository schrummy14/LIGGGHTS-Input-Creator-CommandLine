import numpy as np
import helpers as hp

class particle():
    def __init__(self):
        self.template = []
        
    def getPartOpts(self,simProps):
        hp.clear()
        while True:
            print("Number of Templates Defined: " + str(len(self.template)))
            print("1: Define Particle Template")
            print("2: Define ")
            return