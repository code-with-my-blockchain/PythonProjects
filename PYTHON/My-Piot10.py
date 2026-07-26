import pandas as pd
import matplotlib.pyplot as plt

try:
    df = pd.read_csv("data.csv")
    print("File loaded successfully!")
except FileNotFoundError:
    print("Error: data.csv not found. Make sure it's in the same folder.")
    exit()

type_count = df["Type 1"].value_counts(ascending=True)

plt.barh(type_count.index, type_count.values, 
         color="#4a90e2", 
         edgecolor="black")


plt.title("Number of Pokemon by Primary Type")
plt.xlabel("Count")
plt.ylabel("Type")
plt.tight_layout()

plt.show()