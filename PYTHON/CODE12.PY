import time

timestamp = time.strftime('%H:%M:%S')
print(timestamp)

timestamp = int(time.strftime('%H'))
print(timestamp) 

timestamp = time.strftime('%M')
print(timestamp) 

timestamp = time.strftime('%S')
print(timestamp) 

import time

name = input("Enter your name: ")

hour = int(time.strftime('%H'))

if hour >= 0 and hour < 12:
    print("Hello", name, "Good Morning Sir")
elif hour >= 12 and hour < 17:
    print("Hello", name, "Good Afternoon Sir")
else:
    print("Hello", name, "Good Evening Sir")