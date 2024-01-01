# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 21:01:00 2021

@author: david
"""

class Goat:
       
    def __init__(self,name,age,num_legs):
        self.name=name
        self.age=age
        self.num_legs=num_legs

    def description(self):
        print(self.name + " is " + str(self.age) + " years old and has " + str(self.num_legs) + " legs"  )

    def eats(self,food):
        print(self.name + " eats " + food)