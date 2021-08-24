import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import random

class IsolationForestModel:

    def __init__(self):

        self.model = None
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

        self.model = IsolationForest(n_estimators=1000, max_samples='auto', contamination=self.contamination, n_jobs=-1, random_state=123)
        train_contaminated_data = self._add_contaminated_data(train_data)
        self.model.fit(X=train_contaminated_data)
        anomaly_score = self.model.score_samples(X=train_contaminated_data)
        self.quantile_01 = np.quantile(anomaly_score, q=self.contamination)



    def detectAnomaly(self, input_data):

        anomaly = False

        prediction = self.model.predict(X=input_data)

        score = self.model.score_samples(X=input_data)


        if (prediction == -1):
            anomaly = True

        self._last_prediction_log = """ *** PCA PREDICTION REPORT *** """
        self._last_prediction_log += """\n Input Data: \n"""
        self._last_prediction_log += input_data.to_string()
        self._last_prediction_log += """\n\n Anomaly Score for the input data: \n"""
        self._last_prediction_log += str(score)
        self._last_prediction_log += """\n\n Anomaly Result: \n"""
        self._last_prediction_log += str(anomaly)
        self._last_prediction_log += """\n\n"""

        return anomaly


    def get_log(self):
        return self._last_prediction_log
