
happy = True
print("Example 1 Output:", happy) 


foods = list()
print("\nAb food items (or write 'quit' ):")
while True:
  food = input("> ")
  if food == "quit":
      break
  foods.append(food)
print("your list:", foods)

numbers = [1, 2, 3, 4, 5]
n = len(numbers)
print("\nNumbers reverse order mein:")
while n > 0:
    print(numbers.pop())
    n = len(numbers)