import sys
sys.path.append('../src/')
import pandas as pd
import random
import os
import GMM_model
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns




dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../dataset/init_data.csv')

datos = pd.read_csv(filename)
train, test = train_test_split(datos, test_size=0.2)


systemGMM = GMM_model.GMMModel(20)
systemGMM.trainModel(train)


fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7, 3.5))
sns.distplot(
    systemGMM.gmmModel.score_samples(X=train),
    hist    = False,
    rug     = True,
    color   = 'blue',
    kde_kws = {'shade': True, 'linewidth': 1},
    ax      = ax
)

ax.set_title('Distribución predicciones')
ax.set_xlabel('Logaritmo densidad de probabilidad');
plt.draw()
plt.show()

count = 0
for i in range(0, len(test.index)):
    result = systemGMM.detectAnomaly(test.iloc[[i]])
    if (result == True):
        count = count +  1

print("number of detected anomalies in the test dataset: " + str(count))




