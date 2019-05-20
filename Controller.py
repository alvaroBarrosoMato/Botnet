from flask import Flask
from flask import json
from DecisionTree import DecisionTreeClass, hola, construir, test
from NeuralNetwork import NeuralNetwork
from rq import Queue, job
from Worker import conn
import json


app = Flask(__name__)
dtree = DecisionTreeClass()
NeuralNetwork = NeuralNetwork()
dtreeJob = None

dTreeQueue = Queue('dTree', connection=conn)
workersLimit = 10

testdataset = 'testDataset.csv'

dtreeStatus = 'new'
jobList = {}
treeList = {}


class TreeStatsRow:
    name = 0
    buildTime = 0
    aciertos = 0
    fallos = 0
    percAcierto = 0
    def __init__(self, name, buildTime, aciertos, fallos, percAcierto):
        self.name = name
        self.buildTime = buildTime
        self.aciertos = aciertos
        self.fallos = fallos
        self.percAcierto = percAcierto



@app.route("/1")
def test1():
    result = dTreeQueue.enqueue(hola)
    print("result" + result)
    return result

@app.route("/dtree/get/<int:index>")
def getAll(index):

    if (len(treeList) == 0):
        load()
    if (len(treeList) == 0):
        return "Waiting for Algorithms to Build"
    else:
        tree = treeList[index]
        percAcierto = ((tree.aciertos * 100) / (tree.aciertos + tree.fallos))
        stats = TreeStatsRow(tree.name, tree.buildTime, tree.aciertos, tree.fallos, percAcierto)
        jsonObject = json.dumps(stats.__dict__)
        return jsonObject

@app.route("/dtree/load")
def load():
    print(len(jobList))

    while jobList[0].result == None:
        if len(jobList) > 0:
            if len(treeList) == workersLimit:
                return "Algorithms Built and Loaded"
            else:
                i = 0
                while i < len(jobList):
                    treeList[i] = (jobList[i].result)
                    i = i + 1
                dtreeStatus = 'loaded'
                print(len(treeList))
                return "loaded"
    return "Waiting for Algorithms to Build"

@app.route("/dtree/train/<int:index>/<string:dataset>")
def train(index, dataset):
    jobList.append(dTreeQueue.enqueue(construir, dataset + "" + str(index) + ".csv", index))
    return "Training"

@app.route("/dtree/getTime/<int:index>")
def getTime(index):

    if(len(treeList)==0):
        load()
    if (len(treeList) == 0):
        return "Waiting for Algorithms to Build"
    else:
        print("Time = " + str(treeList[1].buildTime))
        print("Time = " + str(treeList[index].buildTime))
        return str(treeList[index].buildTime)


@app.route("/dtree/traintest")
def buildAllMix():
    dtreeStatus = 'training'
    i = 0
    while i < workersLimit:
        jobList[i] = (dTreeQueue.enqueue(construir, "mix.csv", i))
        i = i + 1
    return "training"

@app.route("/dtree/trainAll/<string:dataset>")
def buildAllDTree(dataset):
    dtreeStatus = 'training'
    i = 0
    while i < workersLimit:
        jobList.append(dTreeQueue.enqueue(construir, dataset + "" + str(i) + ".csv", i))
        i = i + 1
    return "training"

@app.route("/dtree/setdataset/<string:dataset>")
def setDataset(dataset):
    testdataset = dataset
    return "New Test Dataset: " + testdataset

@app.route("/dtree/test/<int:index>")
def test(index):
    print("treeList: "+ str(len(treeList)))
    if(len(treeList) >= index):
        tree = treeList[index]
        treeList[index] = dTreeQueue.enqueue(tree.test, "testDataset.csv")
        return "testing"
    else:
        return "Index Out of Bounds"





## Decision Tree
@app.route("/dtree/build/<string:dataset>")
def buildTree(dataset):
    dtree.build(dataset)
    time = dtree.getBuildTime()
    return "time = " + str(time)

@app.route("/dtree/save/<string:filename>")
def saveTree(filename):
    return dtree.saveTree(filename)

@app.route("/dtree/load/<string:filename>")
def loadTree(filename):
    return dtree.loadtree(filename)

@app.route("/dtree/time")
def timeTree():
    time = dtree.getBuildTime()
    return "time = " + str(time)

@app.route("/dtree/graphviz")
def graphviz():
    return dtree.graphviz()

## Decision Tree
@app.route("/neuralnetwork/build/<string:dataset>")
def buildFeatureSelection(dataset):
    NeuralNetwork.build(dataset)
    time = NeuralNetwork.getBuildTime()
    return "time = " + str(time)

@app.route("/neuralnetwork/time")
def timeNeuralNetwork():
    time = NeuralNetwork.getBuildTime()
    return "time = " + str(time)

@app.route("/neuralnetwork/save/<string:filename>")
def saveNeuralNetwork(filename):
    return NeuralNetwork.saveTree(filename)

@app.route("/neuralnetwork/load/<string:filename>")
def loadNeuralNetwork(filename):
    return NeuralNetwork.loadtree(filename)




if __name__ == "__main__":
    app.run()
    jobList = []
    treeList = []

