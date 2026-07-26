class MyClass:
  def __init__(self, value):
      self._value = value
    
  def show(self):
    print(f"Value is {self._value}")
    
  @property
  def ten_value(self):
      return 10 * self._value
      
obj = MyClass(10)
print(obj.ten_value)
obj.show()
class MyClass:
  def __init__(self, value):
      self._value = value
    
  def show(self):
    print(f"Value is {self._value}")
    
  @property
  def value(self):
      return self._value
      
  @value.setter
  def value(self, new_value):
      self._value = new_value/10
      
obj = MyClass(10)
obj.value = 100
print(obj.value)
obj.show()