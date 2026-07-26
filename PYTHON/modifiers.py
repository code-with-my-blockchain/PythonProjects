class Employee:
    def __init__(self):
        self.name = "Ali"

a = Employee()
print(a.name)
class Employee:
    def __init__(self):
        self.__name = "AlI"

a = Employee()
# print(a.__name) # Cannot be accessed directly
print(a._Employee__name) # Can be accessed via Name Mangling
class Student:
    def __init__(self):
        self._name = "Ali"

    def _funName(self):      # protected method
        return "Ali is a programmer"

class Subject(Student):       # inherited class
    pass

obj = Student()
obj1 = Subject()

# calling by object of Student class
print(obj._name)
print(obj._funName())
# calling by object of Subject class
print(obj1._name)
print(obj1._funName())
