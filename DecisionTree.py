# @title
import pandas as pd
import sklearn as sk
import sklearn.tree as classifier
import time
import sklearn.metrics
import pickle
import numpy



from sklearn.tree import export_graphviz


def hola():
    print("Hola Caracola")
    return "Hola Adios"



class DecisionTreeClass:

    rtree = classifier.DecisionTreeClassifier()
    trainData = 0
    features = 0
    start = 0
    end = 0
    predictions = 0
    testData = 0

    def build(self, dataset):
        trainData = pd.read_csv(dataset)
        trainData = trainData.fillna(0)
        self.features = list(trainData.columns[1:])

        self.start = time.time()
        self.rtree.fit(trainData[self.features], trainData["ip"])
        self.end = time.time()

        export_graphviz(self.rtree, out_file='DecisionTree.dot', feature_names=self.features)

        predictions = self.rtree.predict(trainData[self.features])
        value = trainData["ip"]
        return self

    def saveTree(self, fileName):
        pickle.dump(self.rtree, (open(fileName, 'wb')))
        return "Saved"

    def loadtree(self, fileName):
        self.rtree = pickle.load(open(fileName, 'rb'))
        return "Loaded"

    def getBuildTime(self):
        return self.end - self.start

    def graphviz(self):
        f = open('DecisionTree.dot', 'r')
        if f.mode == 'r':
            s = f.read()
            print(s)
            return s
        return

    def predict(self, data):
        self.rtree.predict(data)
        return 1;

    def test(self, fileName, ):
        self.testData = pd.read_csv(fileName)
        self.testData = self.testData.fillna(0)
        self.aciertos = 0
        self.fallos = 0
        i = 0
        l = len(self.testData[self.features])
        while i < l:
            # print (str(predictions[i]) + " - " + str(value[i]) + " / " + str(predictions[i] == value[i]))
            # print(predictions[i] == value[i])
            if self.predictions[i] == self.trainData.iloc[i][0]:
                self.aciertos = self.aciertos + 1
            else:
                self.fallos = self.fallos + 1

            i = i + 1

            print(self.aciertos)
            print(self.fallos)





