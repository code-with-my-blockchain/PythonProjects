import matplotlib.pyplot as plt
import numpy as np

x = np.array([1, 2, 3, 4, 5])

fig, axs = plt.subplots(2, 2)

axs[0, 0].plot(x, x * 2, color="red")
axs[0, 0].set_title("x * 2")

axs[0, 1].plot(x, x ** 2, color="blue")
axs[0, 1].set_title("x ** 2")

axs[1, 0].plot(x, x ** 3, color="green")
axs[1, 0].set_title("x ** 3")

axs[1, 1].plot(x, x ** 4, color="purple")
axs[1, 1].set_title("x ** 4")

plt.tight_layout()

plt.show()