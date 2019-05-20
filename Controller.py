from flask import Flask
from flask import json
from DecisionTree import DecisionTreeClass, hola, construir, test
from NeuralNetwork import NeuralNetwork
from rq import Queue, job
from Worker import conn
import json
import pickle

app = Flask(__name__)
dtree = DecisionTreeClass()

dTreeQueue = Queue('dTree', connection=conn)

jobList = {}
treeList = {}
workersLimit = 10



@app.route("/dtree/traintest")
def buildAllMix():
    i = 0
    while i < workersLimit:
        jobList[i] = construir("mix.csv", i)
        i = i + 1

    while i < workersLimit:
        print(treeList[i].buildTime)
        i = i + 1

    return "Trained"

@app.route("/dtree/train")
def train():
    dtreeStatus = 'training'
    i = 0
    while i < workersLimit:
        jobList[i] = dTreeQueue.enqueue(construir, "mix.csv", i, result_ttl=-1)
        i = i + 1

    result = None
    while(result==None):
        i = 0
        while (i < workersLimit):
            treeList[i] = jobList[i].result
            result = treeList[i]
            if result == None:
                break
            i = i + 1

    i = 0
    while i < workersLimit:
        print(treeList[i].buildTime)
        treeList[i].saveTree('tree' + str(i) + ".pkl")
        i = i + 1

    return "Trained"


@app.route("/dtree/test/<int:index>")
def test(index):
    if len(treeList) >= index:
        treeList[index] = treeList[index].test("testDataset.csv")
        result = treeList[index]
        percAcierto = ((result.aciertos * 100) / (result.aciertos + result.fallos))
        print("Aciertos: " + str(result.aciertos))
        print("fallos: " + str(result.fallos))
        print("percAcierto: " + str(percAcierto))

        return "Tested"
    else:
        return "Index Out of Bounds"


@app.route("/dtree/load")
def loadall(index):
    i = 0
    while i < workersLimit:
        dtree = DecisionTreeClass()
        treeList[i] = dtree.loadTree('tree' + str(i) + ".pkl")
        i = i + 1
    return "Saved"


@app.route("/dtree/getTime/<int:index>")
def getTime(index):

    if (len(treeList) == 0):
        return "Waiting for Algorithms to Build"
    else:
        print("Time = " + str(treeList[index].buildTime))
        return str(treeList[index].buildTime)


@app.route("/dtree/save/<int:index>")
def save(index):

    if (len(treeList) == 0):
        return "Waiting for Algorithms to Build"
    else:
        treeList[index].saveTree('tree.pkl')
        return "Saved"

@app.route("/dtree/load/<int:index>")
def load(index):

    if (len(treeList) == 0):
        return "Waiting for Algorithms to Build"
    else:
        treeList[index].loadTree('tree.pkl')
        return "Saved"

if __name__ == "__main__":
    app.run()
