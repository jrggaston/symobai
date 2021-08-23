import sys
sys.path.append('../src/')
import pandas as pd
import random
import os
import isolationForest_model
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../dataset/init_data.csv')

datos = pd.read_csv(filename)
train, test = train_test_split(datos, test_size=0.2)

systemIsFo = isolationForest_model.IsolationForestModel()
systemIsFo.trainModel(train)


score_anomalia = systemIsFo.isFo.score_samples(X=train)
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7, 3.5))
sns.distplot(
    score_anomalia,
    hist    = False,
    rug     = True,
    color   = 'blue',
    kde_kws = {'shade': True, 'linewidth': 1},
    ax      = ax
)
cuantil_01 = np.quantile(score_anomalia, q=0.01)
ax.axvline(cuantil_01, c='red', linestyle='--', label='cuantil 0.01')
ax.set_title('Distribución de los valores de anomalía')
ax.set_xlabel('Score de anomalía');
plt.draw()

plt.show()





count = 0
for i in range(0, len(test.index)):


    anomaly = systemIsFo.detectAnomaly([test.iloc[i]])
#    print([train.iloc[i]])
    if (anomaly == True):
        count = count +  1

    #print(anomaly)
    #print("Anomaly with train data: " + str(anomaly))
    #datos = datos.iloc[[i]].copy()

    #datos.loc[i, 'tx_bytes'] = 100000
    #datos.loc[i, 'rx_bytes'] = 100000
    #datos.loc[i, 'timestamp'] = 0

    #anomaly = systemIsFo.detectAnomaly([datos.loc[i]])
    #print("Anomaly with modified data: " + str(anomaly))

print("number of detected anomalies in the test dataset: " + str(count))


