import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import random

class IsolationForestModel:

    def __init__(self):

        self.isFo = None
        self.quantile_01 = 0
        self.contamination = 0.01

    def _add_contaminated_data(self, input_data):

        data = input_data.copy()

        mean_data = (np.trunc(data.max(axis=0)) + 1)
        rows_to_add = int(len(data.index) * self.contamination)
        for i in range(0, rows_to_add):
            wrong_data = mean_data * random.randint(10, 20)
            wrong_df = pd.DataFrame([wrong_data], columns=data.columns)
            data = data.append(wrong_df, ignore_index=True)

        return data

    def trainModel(self, train_data):

        self.isFo = IsolationForest(n_estimators=1000, max_samples='auto', contamination=self.contamination, n_jobs=-1, random_state=123)
        train_contaminated_data = self._add_contaminated_data(train_data)
        self.isFo.fit(X=train_contaminated_data)
        anomaly_score = self.isFo.score_samples(X=train_contaminated_data)
        self.quantile_01 = np.quantile(anomaly_score, q=self.contamination)



    def detectAnomaly(self, input_data):

        anomaly = False

        prediction = self.isFo.predict(X=input_data)

        if (prediction == -1):
            anomaly = True

        return anomaly


if (__name__ == '__main__'):


    datos_X = pd.read_csv("collected_data2.csv")

    systemIsFo = IsolationForestModel()
    systemIsFo.trainModel(datos_X)

    for i in range (0, 10):
        datos = datos_X.iloc[[i]].copy()

        #datos.loc[i, 'tx_bytes'] = 10000
        datos.loc[i, 'rx_bytes'] = 10000
        datos.loc[i, 'timestamp'] = 0



        #print(datos)
        val = systemIsFo.modelData(datos)
        print(val)


