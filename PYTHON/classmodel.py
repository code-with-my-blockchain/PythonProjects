class Employee:
  company = "Apple"
  def show(self):
    print(f"The name is {self.name} and company is {self.company}")

  @classmethod
  def changeCompany(cls, newCompany):
    cls.company = newCompany


e1 = Employee()
e1.name = "ALI"
e1.show()
e1.changeCompany("Tesla")
e1.show()
print(Employee.company)
class Employee:
  company = "Apple"
  def show(self):
    print(f"The name is {self.name} and company is {self.company}")

  @classmethod
  def changeCompany(cls, newCompany):
    cls.company = newCompany


e1 = Employee()
e1.name = "ALI"
e1.show()

e2 = Employee() 
e2.name = "Awais"
e2.show()

e1.changeCompany("Tesla")
e1.show()
e2.show() 