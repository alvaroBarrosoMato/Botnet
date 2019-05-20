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

jobList = []
treeList = []
workersLimit = 10


@app.route("/dtree/test/<int:index>")
def test(index):
    print("treeList: "+ str(len(treeList)))
    if len(treeList) >= index:
        tree = treeList[index]
        treeList[index] = dTreeQueue.enqueue(tree.test, "testDataset.csv")
        return "testing"
    else:
        return "Index Out of Bounds"

@app.route("/dtree/size")
def testing():
    print("tree - " + str(len(treeList)))
    print("job - " + str(len(jobList)))
    return "done"


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
        trainJob = dTreeQueue.enqueue(construir, "mix.csv", i)
        jobList.append(trainJob)
        print(trainJob.get_id())
        i = i + 1

    return "training"

@app.route("/dtree/load")
def load():
    print(len(jobList))
    if len(jobList) > 0:
        if len(treeList) == workersLimit:
            return "Algorithms Built and Loaded"
        else:
            i = 0
            while i < len(jobList):
                treeList.append(jobList[i].result)
                i = i + 1
            dtreeStatus = 'loaded'
            print(len(treeList))
            return "loaded"
    return "Waiting for Algorithms to Build"

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    trainJob = job.fetch(job_key, connection=conn)

    if trainJob.is_finished:
        return str(trainJob.result), 200
    else:
        return "Nay!", 202


if __name__ == "__main__":
    app.run()
