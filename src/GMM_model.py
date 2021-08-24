import pandas as pd
from sklearn.mixture import GaussianMixture
import random

class GMMModel:

    def __init__(self, number_of_components):

        self.gmmModel = None
        self._max_number_of_components = number_of_components
        self._covariance_type = ['spherical', 'tied', 'diag', 'full']
        self._min_prob = None
        self._last_prediction_log = ""

    def _GMMModel(self, input_data, components, covariance_type):

        gmm_model = GaussianMixture(
            n_components=components,
            covariance_type=covariance_type,
            random_state=123,
            reg_covar=1e-5
        )

        gmm_model.fit(X=input_data)

        return gmm_model

    def _GMMAnalysis(self, input_data):

        n_components = range(1, self._max_number_of_components)

        min_cov_type = None
        min_cov_components = -1
        min_cov = -1

        for covariance_type in self._covariance_type:
            bic = []

            for i in n_components:
                model = self._GMMModel(input_data, i, covariance_type)
                model_data = model.bic(input_data)
                bic.append(model_data)
                if min_cov == -1 or model_data < min_cov:
                    min_cov_type = covariance_type
                    min_cov_components = i
                    min_cov = model_data

        return min_cov_type, min_cov_components

    def trainModel(self, input_data):

        cov_type, comp = self._GMMAnalysis(input_data)

        self.gmmModel = self._GMMModel(input_data, comp, cov_type)

        log_prob = self.gmmModel.score_samples(X=input_data)
        self._min_prob = min(log_prob)


    def detectAnomaly(self, input_data):

        anomaly = False

        log_test = self.gmmModel.score_samples(X=input_data)
        if (log_test < self._min_prob):
            #print("log is " + str(log_test) + " and min prob is: "+ str(self._min_prob))
            anomaly = True

        self._last_prediction_log = """ *** GMM PREDICTION REPORT *** """
        self._last_prediction_log += """\n Input Data: \n"""
        self._last_prediction_log += input_data.to_string()
        self._last_prediction_log += """\n\n Probability log of the prediction: \n"""
        self._last_prediction_log +=  str(log_test)
        self._last_prediction_log += """\n\n Min Prob is : \n"""
        self._last_prediction_log += str(self._min_prob)
        self._last_prediction_log += """\n\n Anomaly Result: \n"""
        self._last_prediction_log += str(anomaly)
        self._last_prediction_log += """\n\n"""


        return anomaly

    def get_log(self):
        return self._last_prediction_log