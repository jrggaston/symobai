import sys
sys.path.append('../src/')
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

import pca_model
from sklearn.model_selection import train_test_split



dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../dataset/init_data.csv')

datos = pd.read_csv(filename)

train, test = train_test_split(datos, test_size=0.2)

systemPCA = pca_model.PCAModel(len(train.columns) - 4)
systemPCA.trainModel(train)

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 4))
ax.bar(
    x=np.arange(systemPCA._pca_named_steps.n_components_) + 1,
    height=systemPCA._pca_named_steps.explained_variance_ratio_
)

print(systemPCA._pca_named_steps.explained_variance_ratio_)

for x, y in zip(np.arange(len(train.columns)) + 1, systemPCA._pca_named_steps.explained_variance_ratio_):
    label = round(y, 2)
    ax.annotate(
        label,
        (x, y),
        textcoords="offset points",
        xytext=(0, 10),
        ha='center'
    )

ax.set_xticks(np.arange(systemPCA._pca_named_steps.n_components_) + 1)
ax.set_ylim(0, 1.1)
ax.set_title('Variance per component')
ax.set_xlabel('Component')
ax.set_ylabel('Percentage')
plt.draw()

# accum variance
acum_variance = systemPCA._pca_named_steps.explained_variance_ratio_.cumsum()
print('Accumulated variance')
print(acum_variance)

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 4))
ax.plot(
    np.arange(systemPCA.number_of_components) + 1,
    acum_variance,
    marker='o'
)

for x, y in zip(np.arange(len(train.columns)) + 1, acum_variance):
    label = round(y, 2)
    ax.annotate(
        label,
        (x, y),
        textcoords="offset points",
        xytext=(0, 10),
        ha='center'
    )

ax.set_ylim(0, 1.1)
ax.set_xticks(np.arange(systemPCA._pca_named_steps.n_components_) + 1)
ax.set_title('% of acum variance')
ax.set_xlabel('Component')
ax.set_ylabel('Acum variance')
plt.draw()



plt.show()



#wrong_data = [random.uniform(0, 1) * 10 for i in range(0, 12)]
#dframe_test = pd.DataFrame([wrong_data], columns=datos.columns)

#print("Result with wrong data: " + str(systemPCA.detectAnomaly((dframe_test))))

count = 0
for i in range(0, len(test.index)):
    result = systemPCA.detectAnomaly(test.iloc[[i]])
    if (result == True):
        count = count +  1

print("number of detected anomalies in the test dataset: " + str(count))


