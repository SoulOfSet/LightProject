import os

import board
import flask
import yaml
from flask import Flask, request, jsonify
from py_eureka_client import eureka_client

import colors
from gpio.led_manager import LedManager

is_neopixel = True
try:
    import neopixel
except ImportError:
    print("No neopixel")
    is_neopixel = False

# Create Flask object called app.
app = Flask(__name__)

# Directory for config file
config_dir = os.path.dirname(os.path.realpath(__file__)) + os.sep

# Attempt to load the config file and assign it to the appropriate variables
hostname = port = app_name = eureka_port = eureka_hostname = None

try:
    with open(config_dir + os.sep + "config.yml") as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        hostname = config['hostname']
        port = config['port']
        app_name = config['app_name']
        eureka_port = config['eureka_port']
        eureka_hostname = config['eureka_hostname']
except Exception as e:
    print("Unable to load config file")
    exit(1)

curr_thread = None

if is_neopixel:
    led_manager = LedManager(False, board.D18, 0.75, 100)
else:
    led_manager = LedManager(True, "D18", 0.75, 100)


@app.route('/set_color', methods=['GET'])
def set_color():
    color = request.args.get('color')
    is_color = led_manager.fill_color(color)
    if is_color:
        return flask.Response(status=200)
    else:
        return flask.Response(status=500)


@app.route('/set_procedure', methods=['GET'])
def set_procedure():
    procedure = request.args.get('procedure')
    is_real_proc = led_manager.start_procedure(procedure)
    if is_real_proc:
        return flask.Response(status=200)
    else:
        return flask.Response(status=500)


@app.route('/get_procedures', methods=['GET'])
def get_procedures():
    return jsonify(list(led_manager.get_procedures()))


@app.route('/get_colors', methods=['GET'])
def get_colors():
    return jsonify(list(colors.COLORS.keys()))


if __name__ == '__main__':
    eureka_client.init_registry_client(eureka_server="http://" + eureka_hostname + ":" + eureka_port + "/eureka",
                                       app_name=app_name,
                                       instance_port=port)
    app.run(host=hostname, port=port)
