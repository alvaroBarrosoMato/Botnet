from flask import Flask
from flask import json
from DecisionTree import DecisionTreeClass, hola
from NeuralNetwork import NeuralNetwork

from rq import Queue
from Worker import conn

app = Flask(__name__)
dtree = DecisionTreeClass()
NeuralNetwork = NeuralNetwork()

q = Queue(connection=conn)

@app.route("/")
def index():
    return "Index!"

@app.route("/1")
def test1():
    result = q.enqueue(hola)
    return result
@app.route("/2")
def test2():
    result = q.enqueue(dtree.build, "2dataset.csv")
    return "time = " + str(result)
@app.route("/3")
def test3():
    result = q.enqueue(dtree.build, "2dataset.csv")
    return "Index!"



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

