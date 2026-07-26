marks = [3, 5, 6, "Harry", True, 6, 7 , 2, 32, 345, 23]
# print(marks)
# print(type(marks))
# print(marks[0])
# print(marks[1])
# print(marks[2])
# print(marks[3])
# print(marks[4])
# print(marks[5])

# print(marks[-3]) # Negative index
# print(marks[len(marks)-3]) # Positive index mein convert karne ka tarika
# print(marks[5-3]) # Example calculation
# print(marks[2])
# if "6" in marks:
#   print("Yes")
# else:
#   print("No")

# Same apply for strings
# if "Ha" in "Ali":
#   print("Yes")
# print(marks)
# print(marks[1:9])
# print(marks[1:9:3])

lst = [i*i for i in range(10)]
print(lst)
lst = [i*i for i in range(10) if i%2==0]
print(lst)
