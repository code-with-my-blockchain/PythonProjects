import matplotlib.pyplot as plt

categories = ["Freshman", "Sophomores", "Juniors", "Seniors"]

values = [300, 250, 275, 225]

colors = ["red", "yellow", "blue", "green"]

explode = [0, 0, 0, 0.2] 

plt.pie(values, 
        labels=categories, 
        autopct="%1.1f%%", 
        colors=colors, 
        explode=explode, 
        shadow=True, 
        startangle=90)

plt.title("School Of Thoughts")
plt.show()