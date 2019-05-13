from flask import Flask
from DecisionTree import DecisionTreeClass

myApp = Flask(__name__)


@myApp.route("/")
def index():
    dtree = DecisionTreeClass()
    return "Index!"

@myApp.route("/build")
def build():
    dtree.build("dataset2.csv")
    time = dtree.getBuildTime()
    return "time = " + str(time)

@myApp.route("/load")
def load():
    dtree.loadtree()
    return 'loaded'

@myApp.route("/time")
def time():
    time = dtree.getBuildTime()
    return "time = " + str(time)

@myApp.route("/members")
def members():
    return "Members"



if myApp == "__main__":
    myApp.run()


