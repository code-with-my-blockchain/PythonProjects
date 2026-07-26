import matplotlib.pyplot as plt
import numpy as np

x = np.array([2023, 2024, 2025, 2026])

y1 = np.array([15, 25, 30, 20])
y2 = np.array([17, 23, 38, 5])
y3 = np.array([13, 15, 20, 30])

line_style = dict(
    marker='.', 
    markersize=30, 
    linestyle='solid', 
    linewidth=4
)

plt.plot(x, y1, color='#f0de18', **line_style)
plt.plot(x, y2, color='#0ef0d5', **line_style)
plt.plot(x, y3, color='#4ef00e', **line_style)

plt.title("Class Sizes Comparison", fontsize=20, fontweight='bold')
plt.xlabel("Year", fontsize=15)
plt.ylabel("Students", fontsize=15)

plt.xticks(x)

plt.show()