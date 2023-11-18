from flask import Flask, jsonify
from getLastData import getData, getOutsideTemp


app = Flask(__name__)


@app.route('/values')
def get_values():
    values=[getData()]
    return jsonify(values)


@app.route('/tempout')
def get_tempout():
    values=[getOutsideTemp()]
    return jsonify(values)


@app.route('/')
def show_info():
    return 'usage: url?/values'
