import pandas as pd
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import random
import numpy as np


class PCAModel:

    def __init__(self, number_of_components):

        self.number_of_components = number_of_components
        self.model = None
        self._pca_named_steps = None
        self._last_prediction_log = ""
        #self.scaler = None
        pass

    def trainModel(self, input_data):

        #self.scaler = StandardScaler().fit(input_data)

        # PCA training. It is required to do a standarization
        self.model = make_pipeline(StandardScaler(), PCA(n_components=self.number_of_components))
        self.model.fit(input_data)
        self._pca_named_steps = self.model.named_steps['pca']


    def detectAnomaly(self, input_data):

        anomaly = False

        index_aux = ["PC" + str(i) for i in range(1, self.number_of_components + 1)]

        transform_data = self.model.transform(X=input_data)
        transform_data = pd.DataFrame(transform_data, columns=index_aux, index=input_data.index)

        modeled = self.model.inverse_transform(X=transform_data)
        modeled = pd.DataFrame(modeled, columns=input_data.columns,index=input_data.index )

        #error_std = abs(self.scaler.transform(input_data)**2 - self.scaler.transform(modeled)**2)
        error = abs((input_data)**2 - (modeled)**2)
        error_percentage = (error).div(input_data**2)
        error_percentage.replace([np.inf, -np.inf], 0, inplace=True)

        sum_error = error_percentage.iloc[0].sum()

        #print(sum_error)
        self._last_prediction_log = """ *** PCA PREDICTION REPORT *** """
        self._last_prediction_log += """\n Input Data: \n"""
        self._last_prediction_log += input_data.to_string()
        self._last_prediction_log += """\n\n Transformed Data: \n"""
        self._last_prediction_log +=  modeled.to_string()
        self._last_prediction_log += """\n\n Error: \n"""
        self._last_prediction_log += error.to_string()
        self._last_prediction_log += """\n\n Accumulated Error: \n"""
        self._last_prediction_log += str(sum_error)
        self._last_prediction_log += """\n\n Anomaly Result: \n"""
        self._last_prediction_log += str(anomaly)
        self._last_prediction_log += """\n\n"""

        #this threshold is empiric
        if (sum_error > 10):
            anomaly = True


        return anomaly

    def get_log(self):
        return self._last_prediction_log

