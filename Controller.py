from flask import Flask
from flask import json
from DecisionTree import DecisionTreeClass, hola, construir
from NeuralNetwork import NeuralNetwork
from rq import Queue, job
from Worker import conn


app = Flask(__name__)
dtree = DecisionTreeClass()
NeuralNetwork = NeuralNetwork()
dtreeJob = None
treeList = []

dTreeQueue = Queue('dTree', connection=conn)
workersLimit = 10


@app.route("/")
def index():
    return "Index!"

@app.route("/1")
def test1():
    result = dTreeQueue.enqueue(hola)
    print("result" + result)
    return result
@app.route("/build/<int:index>")
def test2(index):
    dtreeJob = dTreeQueue.enqueue(construir, "mix.csv", index)
    return "Construyendo"

@app.route("/getTime/<int:index>")
def test3(index):
    print(len(treeList))
    print("Time = " + str(treeList[1].buildTime))
    print("Time = " + str(treeList[index].buildTime))
    return "Time = " + str(treeList[index].buildTime)

@app.route("/4")
def buildAllDTree():
    i = 0
    while i < workersLimit:
        dtreeJob = dTreeQueue.enqueue(construir, "mix.csv", i)
        dtree = dtreeJob.result
        treeList.append(dtree)
        i = i + 1

    return "Construyendo"


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

