import matplotlib.pyplot as plt
import numpy as np

x = np.array([2023, 2024, 2025, 2026])
y = np.array([15, 25, 30, 20])

colors = ['#FF5733', '#33FF57', '#3357FF', '#F333FF'] 

for i in range(len(x)):
    plt.plot(x[i], y[i], marker='.', markersize=30, color=colors[i])

plt.plot(x, y, color='gray', linestyle='--', linewidth=1, zorder=0)

plt.title("Class Size (Yearly Colors)", fontsize=20, fontweight='bold')
plt.xlabel("Year", fontsize=15)
plt.ylabel("Students", fontsize=15)
plt.xticks(x)

plt.tight_layout()
plt.show()