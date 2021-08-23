import pandas as pd
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import random
import numpy as np


class PCAModel:

    def __init__(self, number_of_components):

        self.number_of_components = number_of_components
        self.pca_model = None
        self._pca_named_steps = None
        #self.scaler = None
        pass

    def trainModel(self, input_data):

        #self.scaler = StandardScaler().fit(input_data)

        # PCA training. It is required to do a standarization
        self.pca_model = make_pipeline(StandardScaler(), PCA(n_components=self.number_of_components))
        self.pca_model.fit(input_data)
        self._pca_named_steps = self.pca_model.named_steps['pca']


    def detectAnomaly(self, input_data):

        anomaly = False

        index_aux = ["PC" + str(i) for i in range(1, self.number_of_components + 1)]

        transform_data = self.pca_model.transform(X=input_data)
        transform_data = pd.DataFrame(transform_data, columns=index_aux, index=input_data.index)

        modeled = self.pca_model.inverse_transform(X=transform_data)
        modeled = pd.DataFrame(modeled, columns=input_data.columns,index=input_data.index )

        #error_std = abs(self.scaler.transform(input_data)**2 - self.scaler.transform(modeled)**2)
        error = abs((input_data)**2 - (modeled)**2)
        error_percentage = (error).div(input_data**2)
        error_percentage.replace([np.inf, -np.inf], 0, inplace=True)

        sum_error = error_percentage.iloc[0].sum()

        #print(sum_error)

        #this threshold is empiric
        if (sum_error > 10):
            anomaly = True


        return anomaly


