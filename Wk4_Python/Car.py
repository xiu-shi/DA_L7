# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 19:23:36 2021

@author: david
"""

class Car:
    
    numWheels = "4" 
    def __init__(self,color,make,fuelType):
        self.make=make
        self.fuelType=fuelType
        self.color=color
        
    def __str__(self):
        return f"This {self.make} car has{self.numWheels} is {self.color} in Color and uses {self.fuelType}"
    
    
    def drive(self,direction):
        return f"{self.make} drives {direction}"
    
    
car1 = Car("Blue","BMW","Petrol")
print(car1)
print(car1.drive("left"))