class Employee:
  def __init__(self, name, id):
    self.name = name
    self.id = id

class Programmer(Employee):
  def __init__(self, name, id, lang):
    super().__init__(name, id)
    self.lang = lang

Awais = Employee("Awais", "420")
Ali = Programmer("Ali", "2345", "Python")
print(Ali.name)
print(Ali.id)
print(Ali.lang)


class ParentClass:
    def parent_method(self):
        print("This is the parent method.")

class ChildClass(ParentClass):
    def child_method(self):
        print("This is the child method.")
        super().parent_method()

child_object = ChildClass()
child_object.child_method()