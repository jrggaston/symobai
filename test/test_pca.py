import sys
sys.path.append('../src/')
import pandas as pd
import random
import os
import pca_model
from sklearn.model_selection import train_test_split



dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../dataset/init_data.csv')

datos = pd.read_csv(filename)

train, test = train_test_split(datos, test_size=0.2)

systemPCA = pca_model.PCAModel(len(datos.columns) - 4)
systemPCA.trainModel(train)


#wrong_data = [random.uniform(0, 1) * 10 for i in range(0, 12)]
#dframe_test = pd.DataFrame([wrong_data], columns=datos.columns)

#print("Result with wrong data: " + str(systemPCA.detectAnomaly((dframe_test))))

count = 0
for i in range(0, len(test.index)):
    result = systemPCA.detectAnomaly(test.iloc[[i]])
    if (result == True):
        count = count +  1

print("number of detected anomalies in the test dataset: " + str(count))


