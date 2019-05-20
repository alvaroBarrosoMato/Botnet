from flask import Flask
from flask import json
from DecisionTree import DecisionTreeClass, hola, construir, test
from NeuralNetwork import NeuralNetwork
from rq import Queue, job
from Worker import conn
import pika, os, urlparse

import json

app = Flask(__name__)
dtree = DecisionTreeClass()

dTreeQueue = Queue('dTree', connection=conn)



# Parse CLODUAMQP_URL (fallback to localhost)
url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
url = urlparse.urlparse(url_str)
params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:], credentials=pika.PlainCredentials(url.username, url.password))
connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='', routing_key='hello', body='Hello CloudAMQP!')
print (" [x] Sent 'Hello World!'")


def callback(ch, method, properties, body):
  print ( " [x] Received %r" % (body))

channel.basic_consume(callback, queue='hello', no_ack=True)

channel.start_consuming()

connection.close()

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
