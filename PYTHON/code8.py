fruit = "Mango"
len1 = len(fruit)
print("Mango is a", len1, "letter word.")

pie = "ApplePie"
print(pie[:5])
print(pie[6])	#returns character at specified index

pie = "ApplePie"
print(pie[:5])      #Slicing from Start
print(pie[5:])      #Slicing till End
print(pie[2:6])     #Slicing in between
print(pie[-8:])     #Slicing using negative index

alphabets = "ABCDE"
for i in alphabets:
    print(i)