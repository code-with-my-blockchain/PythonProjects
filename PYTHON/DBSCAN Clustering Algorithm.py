import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

def points_in_circum(r, n=100):
    return np.array([(math.cos(2*math.pi/n*i)*r + np.random.normal(-30, 30),
                      math.sin(2*math.pi/n*i)*r + np.random.normal(-30, 30)) for i in range(1, n+1)])

df1 = points_in_circum(500, 1000)
df2 = points_in_circum(300, 700)
df3 = points_in_circum(100, 300)

df = np.vstack([df1, df2, df3])
data_frame = pd.DataFrame(df)

plt.figure(figsize=(6, 6))
plt.scatter(data_frame[0], data_frame[1], s=15, color='purple')
plt.title('Sample Dataset')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()

kmeans = sklearn.cluster.KMeans(n_clusters=4, random_state=42)
kmeans.fit(data_frame[[0, 1]])
data_frame['Kmeans_labels'] = kmeans.labels_
colors = ['purple', 'red', 'blue', 'green']

plt.figure(figsize=(6, 6))
plt.scatter(data_frame[0], data_frame[1], c=data_frame['Kmeans_labels'],
            cmap=plt.cm.colors.ListedColormap(colors), s=15)
plt.title('K means Clustering', fontsize=20)
plt.xlabel('Feature 1', fontsize=14)
plt.ylabel('Feature 2', fontsize=14)
plt.show()

import sklearn.cluster # type: ignore
model = sklearn.cluster.AgglomerativeClustering(n_clusters=4, metric='euclidean')
model.fit(data_frame[[0, 1]])

data_frame['hr_labels'] = model.labels_
plt.figure(figsize=(6, 6))
plt.scatter(data_frame[0], data_frame[1], c=data_frame['hr_labels'],
            cmap=plt.cm.colors.ListedColormap(colors), s=15)
plt.title('Hierarchical Clustering', fontsize=20)
plt.xlabel('Feature 1', fontsize=14)
plt.ylabel('Feature 2', fontsize=14)
plt.show()

dbscan = sklearn.cluster.DBSCAN(eps=30, min_samples=6)
dbscan.fit(data_frame[[0, 1]])

data_frame['DBSCAN_opt_labels'] = dbscan.labels_
print(data_frame['DBSCAN_opt_labels'].value_counts())

plt.figure(figsize=(6, 6))
plt.scatter(data_frame[0], data_frame[1], c=data_frame['DBSCAN_opt_labels'],
            cmap=plt.cm.colors.ListedColormap(colors), s=15)
plt.title('DBSCAN Clustering', fontsize=20)
plt.xlabel('Feature 1', fontsize=14)
plt.ylabel('Feature 2', fontsize=14)
plt.show()
