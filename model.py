import pandas as pd
import pca_model
import isolationForest_model
import GMM_model
import os
import random


class Model():

    def __init__(self, train_data):
        ''' Initialize model with the init paramters'''
        self.pca = None
        self.isolation_forest = None
        self.gmm = None

        self.update_model(train_data)


    def get_prediction(self, data):

        ''' Evaluate the model'''
        if self.pca != None:
            pca_prediction = self.pca.detectAnomaly(data)
            if pca_prediction == True:
                print("ERROR: PCA")


        if self.isolation_forest != None:
            isolationForest_prediction = self.isolation_forest.detectAnomaly(data)
            if isolationForest_prediction == True:
                print("ERROR: ISOLATION FOREST")

        if self.gmm != None:
            gmm_prediction = self.gmm.detectAnomaly(data)
            if gmm_prediction == True:
                print("ERROR: GMM")

        return pca_prediction or isolationForest_prediction or gmm_prediction

    def update_model(self, train_file):

        ''' update the model with the new paramters'''

        if os.path.isfile(train_file):
            train_dataset = pd.read_csv(train_file)

            self.pca = pca_model.PCAModel(len(train_dataset.columns) - 3)
            self.pca.trainModel(train_dataset)

            self.isolation_forest = isolationForest_model.IsolationForestModel()
            self.isolation_forest.trainModel(train_dataset)

            self.gmm = GMM_model.GMMModel(20)
            self.gmm.trainModel(train_dataset)

        else:
            raise("ERROR: update model requires a csv as input file to train the model")





if (__name__ == '__main__'):

    file = "collected_data2.csv"

    datos = pd.read_csv(file)

    wrong_data = [random.uniform(0, 1) * 10 for i in range(0, 12)]
    dframe_test = pd.DataFrame([wrong_data], columns=datos.columns)

    m = Model(file)
    print(m.get_prediction(dframe_test))
    print(m.get_prediction(datos.iloc[[2]]))



