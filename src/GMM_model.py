import pandas as pd
from sklearn.mixture import GaussianMixture
import random

class GMMModel:

    def __init__(self, number_of_components):

        self.gmmModel = None
        self._max_number_of_components = number_of_components
        self._covariance_type = ['spherical', 'tied', 'diag', 'full']
        self._min_prob = None

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
            anomaly = True

        return anomaly

