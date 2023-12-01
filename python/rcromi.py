#!/usr/bin/env python3
from flask import Flask
from flask import render_template
from flask import redirect
from subprocess import call
app = Flask(__name__)
app.debug = True

from romi_interface.romi import Romi
romi = Romi()

import json

from controller import Odometer
import time as time
odo = Odometer(romi.read_encoders(), time.time())

@app.route("/")
def hello():
    return render_template("simple.html")

@app.route("/status.json")
def status():
    t = time.time()
    encoders = romi.read_encoders()
    odo.updateOdometry(encoders, t)
    data = {
        "encoders": encoders,
        "odometry": [odo.x, odo.y]
    }
    return json.dumps(data)

@app.route("/motors/<left>,<right>")
def motors(left, right):
    romi.motors(int(left), int(right))
    return ""

if __name__ == "__main__":
    app.run(host = "0.0.0.0")
