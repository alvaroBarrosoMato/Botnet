import subprocess


import pandas as pd
import sklearn as sk
from sklearn.neural_network import MLPClassifier
import time
import pickle

class NeuralNetwork:

    trainData = 0
    features = 0
    start = 0
    end = 0
    neuralClasifier = 0
    time = 0
    predictions = 0
    testData = 0



#    export_graphviz(neuralClasifier, out_file='NeuralNetwork.dot', feature_names=features)

    def build(self, dataset):
        self.trainData = pd.read_csv(dataset)
        self.trainData = self.trainData.fillna(0)
        self.features = list(self.trainData.columns[1:])

        self.neuralClasifier = MLPClassifier(solver='lbfgs')


        self.start = time.time()
        self.neuralClasifier = self.neuralClasifier.fit(self.trainData[self.features], self.trainData["ip"])
        self.end = time.time()
        self.time = self.end - self.start

        return self.featureSelectionTime

    def getBuildTime(self):
        return self.end - self.start

    def saveTree(self, fileName):
        pickle.dump(self.neuralClasifier, (open(fileName, 'wb')))
        return "Saved"

    def loadtree(self, fileName):
        self.neuralClasifier = pickle.load(open(fileName, 'rb'))
        return "Loaded"

    def graphviz(self):
        f = open('DecisionTree.dot', 'r')
        if f.mode == 'r':
            s = f.read()
            print(s)
            return s
        return
