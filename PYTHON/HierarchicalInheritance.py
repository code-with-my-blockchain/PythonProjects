
class BaseClass:
  pass

class Derived1(BaseClass):
  pass

class Derived2(BaseClass):
  pass

class Derived3(Derived1):
  pass

class Apple:
  pass

class Mango:
  pass

class Fruit(Apple, Mango):
  pass

class Banana(Fruit):
  pass
class Apple:
  pass

class Mango:
  pass

class Fruit(Apple, Mango):
  pass

class Banana(Fruit):
  pass
class BaseClass:
  def show_base(self):
    print("This is the Base Class")

class Derived1(BaseClass):
  def show_d1(self):
    print("This is Derived Class 1")

class Derived2(BaseClass):
  def show_d2(self):
    print("This is Derived Class 2")

obj1 = Derived1()
obj1.show_base()
obj1.show_d1()

obj2 = Derived2()
obj2.show_base()
obj2.show_d2()