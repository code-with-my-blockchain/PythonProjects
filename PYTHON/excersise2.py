questions = [
    [
        "Which language was used to create Facebook?", "Python", "French", "JavaScript",
        "Php", "None", 4
    ],
    [
        "What is the capital of Pakistan?", "Karachi", "Lahore", "Islamabad",
        "Peshawar", "None", 3
    ],
    [
        "Which planet is known as the Red Planet?", "Earth", "Mars", "Jupiter",
        "Saturn", "None", 2
    ],
    [
        "Who developed Python Programming Language?", "Wick van Rossum", "Rasmus Lerdorf", "Guido van Rossum",
        "Niene Stom", "None", 3
    ],
]

levels = [1000, 2000, 3000, 5000, 10000, 20000, 40000, 80000, 160000, 320000]
money = 0

for i in range(0, len(questions)):
    question = questions[i]
    print(f"\n\nQuestion for Rs. {levels[i]}")
    print(f"a. {question[1]}          b. {question[2]}")
    print(f"c. {question[3]}          d. {question[4]}")
    
    reply = int(input("Enter your answer (1-4) or 0 to quit: "))
    
    if (reply == 0):
        # Agar user quit kare to pichli jeeti hui raqam milay
        if i > 0:
            money = levels[i-1]
        break
        
    if(reply == question[-1]):
        print(f"Correct answer! You have won Rs. {levels[i]}")
        money = levels[i] # Har sahi jawab par money update hogi
    else:
        print("Wrong answer!")
        # Galat jawab par aap money ko 0 ya pichlay kisi level par set kar saktay hain
        if(i >= 4):
            money = 10000
        elif(i >= 9):
            money = 320000
        else:
            money = 0
        break

print(f"\nYour final take home amount is Rs. {money}")