x = 4  # Global variable
print(x)

def hello():
    x = 5  # Local variable
    y = 1  # Local variable
    print(f"The local x is {x}")
    print("Hello harry")

print(f"The global x is {x}")
hello()
x = 10  # Changing global x
print(f"The global x is {x}")
# print(y) # This will cause an error because y is local to hello()
x = 10  # Global variable

def my_function():
    global x
    x = 4  # This now changes the global x
    y = 5  # Local variable
    print(y)

my_function()
print(x)  # This will now print 4
# print(y) # Error: y is not defined (it's local)