import matplotlib.pyplot as plt

x1 = [0, 1, 1, 2, 3, 4, 5, 6, 7, 8]
y1 = [55, 60, 65, 62, 68, 70, 75, 78, 82, 85]

x2 = [0, 1, 2, 2, 3, 4, 5, 6, 7, 8]
y2 = [50, 58, 65, 70, 72, 78, 83, 88, 92, 97]

plt.scatter(x1, y1, color="skyblue", alpha=0.5, s=200, label="Class A")
plt.scatter(x2, y2, color="red", alpha=0.5, s=200, label="Class B")

plt.xlabel("Hours Studied")
plt.ylabel("Grade")
plt.title("Test Scores")

plt.legend()
plt.show()