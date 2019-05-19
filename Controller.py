from flask import Flask
from flask import json
from DecisionTree import DecisionTreeClass, hola, construir
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

dtreeStatus = 'new'
jobList = []
treeList = []


@app.route("/1")
def test1():
    result = dTreeQueue.enqueue(hola)
    print("result" + result)
    return result

@app.route("/dtree/get/<int:index>")
def getAll(index):
    jsonObject = json.dump(treeList[index])
    return jsonObject
@app.route("/dtree/get2/<int:index>")
def getAllv2(index):
    jsonObject = treeList[index]
    return jsonObject.toJSON()

@app.route("/dtree/load")
def load():
    print(len(jobList))
    i = 0
    while i < len(jobList):
        treeList.append(jobList[i].result)
        i = i + 1
    dtreeStatus = 'loaded'
    return "loaded"

@app.route("/dtree/train/<int:index>/<string:dataset>")
def train(index, dataset):
    jobList.append(dTreeQueue.enqueue(construir, dataset + "" + str(index) + ".csv", index))
    return "Training"

@app.route("/dtree/getTime/<int:index>")
def getTime(index):
    print(len(treeList))
    print("Time = " + str(treeList[1].buildTime))
    print("Time = " + str(treeList[index].buildTime))
    return str(treeList[index].buildTime)

@app.route("/dtree/dtree/traintest/")
def buildAllMix():
    dtreeStatus = 'training'
    i = 0
    while i < workersLimit:
        jobList.append(dTreeQueue.enqueue(construir, "mix.csv", i))
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

