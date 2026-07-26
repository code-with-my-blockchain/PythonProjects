a = int(input("Enter any value between 5 and 9: "))

if(a < 5 or a > 9):
  raise ValueError("Value should be between 5 and 9")
a = input("Enter any value between 5 and 9 (or type 'quit'): ")

if a == "quit":
  print("Quitting...")
else:
  a = int(a)
  if(a < 5 or a > 9):
    raise ValueError("Value should be between 5 and 9")
 
