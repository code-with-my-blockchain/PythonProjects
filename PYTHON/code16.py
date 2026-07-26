i = 0
while(i < 3):
  print(i)
  i = i + 1

print("Done with the loop")

i = int(input("Enter the number: "))
while(i <= 38):
  i = int(input("Enter the number: "))
  print(i)

print("Done with the loop")

count = 5
while (count > 0):
  print(count)
  count = count - 1
else:
  print("I am inside else")

  # Exercise Solution (Logic)
while True:
  num = int(input("Enter a positive number (or negative to quit): "))
  print(num)
  if not num > 0:
    break

  