class Person:
  name = "ALI"
  occupation = "Software Developer"
  networth = 10
  def info(self):
    print(f"{self.name} is a {self.occupation}")


a = Person()
a.name = "Awais"
a.occupation = "Accountant"

b = Person()
b.name = "Anam"
b.occupation = "HR"

c = Person()

a.info()
b.info()
c.info()