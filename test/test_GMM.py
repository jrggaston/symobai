import sys
sys.path.append('../src/')
import pandas as pd
import random
import os
import GMM_model
from sklearn.model_selection import train_test_split




dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../dataset/init_data.csv')

datos = pd.read_csv(filename)
train, test = train_test_split(datos, test_size=0.2)


systemGMM = GMM_model.GMMModel(20)
systemGMM.trainModel(train)


count = 0
for i in range(0, len(test.index)):
    result = systemGMM.detectAnomaly(test.iloc[[i]])
    if (result == True):
        count = count +  1

print("number of detected anomalies in the test dataset: " + str(count))




