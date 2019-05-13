from flask import Flask
from DecisionTree import DecisionTreeClass

app = Flask(__name__)
dtree = DecisionTreeClass()


@app.route("/")
def index():
    return "Index!"

@app.route("/build/<string:dataset>'")
def build(dataset):
    dtree.build(dataset)
    time = dtree.getBuildTime()
    return "time = " + str(time)

@app.route("/load")
def load():
    dtree.loadtree()
    return 'loaded'

@app.route("/time")
def time():
    time = dtree.getBuildTime()
    return "time = " + str(time)

@app.route("/save")
def save():
    return dtree.saveTree()


@app.route("/members")
def members():
    return "Members"



if __name__ == "__main__":
    app.run()

