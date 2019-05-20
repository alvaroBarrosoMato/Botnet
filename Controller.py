from flask import Flask
from flask import json
from DecisionTree import DecisionTreeClass, hola, construir, test
from NeuralNetwork import NeuralNetwork
from rq import Queue, job
from Worker import conn
import json

app = Flask(__name__)
dtree = DecisionTreeClass()

dTreeQueue = Queue('dTree', connection=conn)

jobList = {}
treeList = {}
workersLimit = 10



@app.route("/dtree/traintest")
def buildAllMix():
    dtreeStatus = 'training'
    i = 0
    while i < workersLimit:
        jobList[i] = dTreeQueue.enqueue(construir, "mix.csv", i, result_ttl=-1)
        i = i + 1

    result = None
    while(result==None):
        i = 0
        while i < workersLimit:
            treeList[i] = jobList[i].result
            result = treeList[i]
            i = i + 1

    i = 0
    while i < workersLimit:
        print(treeList[i].buildTime)
        i = i + 1

    return "Trained"

@app.route("/dtree/getTime/<int:index>")
def getTime(index):

    if (len(treeList) == 0):
        return "Waiting for Algorithms to Build"
    else:
        print("Time = " + str(treeList[index].buildTime))
        return str(treeList[index].buildTime)

if __name__ == "__main__":
    app.run()
