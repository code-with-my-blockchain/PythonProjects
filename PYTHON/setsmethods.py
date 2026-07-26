# sets = {1, 2, 5, 6}
# sets2 = {3, 6, 7}

# print(sets.union(sets2))
# sets.update(sets2)
# print(sets, sets2)

cities = {"Tokyo", "Madrid", "Berlin", "Delhi"}
cities2 = {"Tokyo", "Seoul", "Kabul", "Madrid"}
# cities3 = cities.union(cities2)
# print(cities3)
# cities.update(cities2)
# print(cities)

# cities3 = cities.intersection(cities2)
# print(cities3)
# cities.intersection_update(cities2)
# print(cities)

# cities3 = cities.symmetric_difference(cities2)
# print(cities3)
# cities.symmetric_difference_update(cities2)
# print(cities)

# cities3 = cities.difference(cities2)
# print(cities3)
# cities.difference_update(cities2)
# print(cities)

cities = {"Tokyo", "Madrid", "Berlin", "Delhi"}
cities2 = {"Seoul", "Kabul"}
print(cities.isdisjoint(cities2))

cities = {"Tokyo", "Madrid", "Berlin", "Delhi"}
cities2 = {"Seoul", "Kabul", "Madrid"}
print(cities.issuperset(cities2))
cities3 = {"Tokyo", "Madrid", "Berlin", "Delhi"}
print(cities.issuperset(cities3))

cities = {"Tokyo", "Madrid", "Berlin", "Delhi"}
cities2 = {"Tokyo", "Madrid"}
print(cities2.issubset(cities))

cities = {"Tokyo", "Madrid", "Berlin", "Delhi"}
cities.add("Helsinki")
print(cities)

cities = {"Tokyo", "Madrid", "Berlin", "Delhi"}
cities.remove("Tokyo")
print(cities)

# cities.remove("Tokyo2") # Throws error
cities.discard("Tokyo2") # Does not throw error
print(cities)

# item = cities.pop()
# print(cities)
# print(item)

# del cities
# print(cities)

# cities.clear()
# print(cities)

info = {"Carla", 19, False, 5.9}
if "Carla" in info:
    print("Carla is present.")
else:
    print("Carla is absent.")