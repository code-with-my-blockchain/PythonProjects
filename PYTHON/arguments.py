def average(a=9, b=1):
  print("The average is ", (a + b) / 2)

average(b=9) # a default 9 rahega
def average(a=9, b=1):
  print("The average is ", (a + b) / 2)

average(b=9, a=21)
def average(a, b, c=1):
  print("The average is ", (a + b + c) / 2)

average(5, 6) # c default 1 le lega
def average(*numbers):
  sum = 0
  for i in numbers:
    sum = sum + i
  print("Average is: ", sum / len(numbers))

average(5, 6, 7, 1)
def average(*numbers):
  sum = 0
  for i in numbers:
    sum = sum + i
  return sum / len(numbers)

c = average(5, 6, 7, 1)
print(c)
