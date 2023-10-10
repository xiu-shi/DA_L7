# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 20:05:53 2021

@author: david
"""

class Dog:
    
    species="Canis Familiaris"
    
    def __init__(self,name,age):
        self.name=name
        self.age=age

    def description(self):
        print(self.name + " is " + str(self.age) + " years old")

    def speak(self,sound):
        print(self.name + " says " + sound)


        
#Dog("Bob",7)
#print(Dog("Bob",7))

#buddy = Dog("Buddy",9)
#miles = Dog("Miles",4)
#print(buddy.age)
#buddy.age = 10
#print(buddy.age)
#buddy.description()
#buddy.speak("Woof, Woof")
#miles.speak("I can speak Human")

"""
print(buddy.name)
print(buddy.age)
print(buddy.species)
print(miles.name)
print(miles.age)
print(miles.species)
"""
