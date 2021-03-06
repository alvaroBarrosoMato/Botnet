# @title
import pandas as pd
import sklearn as sk
import sklearn.tree as classifier
import time
import sklearn.metrics
import pickle
import numpy
import json



from sklearn.tree import export_graphviz


def hola():
    print("Hola Caracola")
    return "Hola Adios"

def construir(dataset, name):
    dtree = DecisionTreeClass(name)
    dtree = dtree.build(dataset, name)
    print("Time - "+str(dtree.buildTime))
    return dtree

def test(tree):
    tree = tree.test("testDataset.csv")
    return tree


class DecisionTreeClass:
    name = 0
    rtree = classifier.DecisionTreeClassifier()
    buildTime = 0
    trainData = None
    features = 0
    start = 0
    end = 0
    testData = 0
    status = "new"
    savefilename = 'tree.pkl'

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __init__(self, name=None):
        rtree = classifier.DecisionTreeClassifier()
        self.name = name
        self.status = "new"


    def build(self, dataset, name):
        self.name = name
        trainData = pd.read_csv(dataset)
        trainData = trainData.fillna(0)
        self.features = list(trainData.columns[1:])

        self.start = time.time()
        self.rtree.fit(trainData[self.features], trainData["ip"])
        self.end = time.time()

        export_graphviz(self.rtree, out_file='DecisionTree.dot', feature_names=self.features)

        self.saveTree(self.savefilename)
        self.buildTime = self.end - self.start
        value = trainData["ip"]
        print(str(name) + " -> " + str(self.buildTime))
        self.status = "trained"
        return self

    def saveTree(self, fileName):
        pickle.dump(self, (open(fileName, 'wb')))
        return "Saved"

    def loadTree(self, fileName):
        self = pickle.load(open(fileName, 'rb'))
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
        return

    def test(self, fileName):

        self.testData = pd.read_csv(fileName)
        self.testData = self.testData.fillna(0)
        self.aciertos = 0
        self.fallos = 0

        tree = self.rtree
        predictions = tree.predict(self.testData[self.features])

        i = 0
        l = len(self.testData[self.features])
        while i < l:
            if predictions[i] == self.testData.iloc[i][0]:
                self.aciertos = self.aciertos + 1
            else:
                self.fallos = self.fallos + 1
            print(str(predictions[i]) + " / " + str(self.testData.iloc[i][0]))
            i = i + 1

        print(self.aciertos)
        print(self.fallos)
        return self




