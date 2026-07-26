# countries = ("Spain", "Italy", "India", "England", "Germany")
# temp = list(countries)
# temp.append("Russia")       #add item 
# temp.pop(3)                 #remove item
# temp[2] = "Finland"         #change item
# countries = tuple(temp)
# print(countries)

countries = ("Pakistan", "Afghanistan", "Bangladesh", "Shri Lanka")
countries2 = ("Vietnam", "India", "China")
southAsia = countries + countries2
print(southAsia)

# Pehle tuple1 ko define karein
tuple1 = (1, 2, 3, 3, 2, 1, 3, 2, 1)

# Ab count method kaam karega
res = tuple1.count(3)
print('Count of 3 in tuple1 is:', res)

res = tuple1.count(3)
# res = tuple1.index(3)
# res = tuple1.index(3, 4, 8)
# res = len(tuple1)
print('Count of 3 in tuple1 is:', res)