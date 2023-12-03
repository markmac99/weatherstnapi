import os
from flask import Flask, jsonify
from getLastData import getData, getOutsideTemp


app = Flask(__name__)


@app.route('/values')
def get_values():
    fname = os.getenv('DATAFILE', default='/home/pi/weather/weatherdata.json')
    values=[getData(fname)]
    return jsonify(values)


@app.route('/tempout')
def get_tempout():
    fname = os.getenv('DATAFILE', default='/home/pi/weather/weatherdata.json')
    values=[getOutsideTemp(fname)]
    return jsonify(values)


@app.route('/')
def show_info():
    return 'usage: url?/values'
