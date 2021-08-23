import sys
sys.path.append('../src/')
import pandas as pd
import random
import os
import isolationForest_model
from sklearn.model_selection import train_test_split

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../dataset/init_data.csv')

datos = pd.read_csv(filename)
train, test = train_test_split(datos, test_size=0.2)

systemIsFo = isolationForest_model.IsolationForestModel()
systemIsFo.trainModel(train)

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


