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


@app.route("/dtree/size")
def testing():
    queued_job_ids = dTreeQueue.job_ids
    queued_jobs = dTreeQueue.jobs
    print('hola')
    print(len(dTreeQueue))
    for ids in queued_job_ids:
        print(ids)
    for jobs in queued_jobs:
            print(jobs.result)
    return "done"

@app.route("/dtree/traintest")
def buildAllMix():
    dtreeStatus = 'training'
    i = 0
    while i < workersLimit:
        dTreeQueue.enqueue(construir, "mix.csv", i, result_ttl=-1)
        i = i + 1
    print("Hola")
    return "training"

if __name__ == "__main__":
    app.run()
