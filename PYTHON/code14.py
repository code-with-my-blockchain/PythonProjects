x = 4

match x:
    case 0:
        print("x is zero")
    case 4:
        print("x is 4")
    case _:
        print("x is something else")
        day = input("Enter day: ")

day = input("Enter day: ")

match day:
    case "Monday":
        print("Start of week")
    case "Friday":
        print("Weekend coming")
    case _:
        print("Normal day")

match x:
    case 10 if x % 2 == 0:
        print("Even and equal to 10")
    case 10:
        print("Only 10")
    case _:
        print("Something else")
