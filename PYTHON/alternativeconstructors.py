class Employee:
  def __init__(self, name, salary):
    self.name = name
    self.salary = salary

  @classmethod
  def fromStr(cls, string):
    return cls(string.split("-")[0], int(string.split("-")[1]))
    

e1 = Employee("Ali", 12000)
print(e1.name)
print(e1.salary)

string = "Awais-12000"
e2 = Employee.fromStr(string)
print(e2.name)
print(e2.salary)

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def from_string(cls, person_str):
        name, age = person_str.split(',')
        return cls(name, int(age))

person = Person.from_string("Arslan, 30")
print(person.name)
print(person.age)