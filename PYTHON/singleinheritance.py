class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        
    def make_sound(self):
        print("Sound made by the animal")

class Cat(Animal):
    def __init__(self, name, color):

        Animal.__init__(self, name, species="Cat")
        self.color = color
        
   
    def make_sound(self):
        print("Meow!")
        
  
    def scratch(self):
        print(f"{self.name} is scratching the sofa!")
        
    
    def sleep(self):
        print(f"The {self.color} cat is sleeping...")


c = Cat("Kitty", "White")

c.make_sound() 
c.scratch()     
c.sleep()       

print(f"Name: {c.name}, Species: {c.species}")
class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        
    def make_sound(self):
        print("Sound made by the animal")

class Dog(Animal):
    def __init__(self, name, breed):
        Animal.__init__(self, name, species="Dog")
        self.breed = breed
        
    def make_sound(self):
        print("Bark!")

d = Dog("Dog", "Doggerman")
d.make_sound()

a = Animal("Dog", "Dog")
a.make_sound()