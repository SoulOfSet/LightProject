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
hostname = port = app_name = eureka_port = eureka_hostname = brightness = start_up_mode = start_up_selection = \
    num_pixels = None

try:
    with open(config_dir + os.sep + "config.sample.yml") as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        hostname = config['hostname']
        port = config['port']
        app_name = config['app_name']
        num_pixels = config['num_pixels']
        eureka_port = config['eureka_port']
        eureka_hostname = config['eureka_hostname']
        brightness = config['brightness']
        start_up_mode = config['start_up_mode']
        start_up_selection = config['start_up_selection']
except Exception as e:
    print("Unable to load config file")
    print(e)
    exit(1)

curr_thread = None

if is_neopixel:
    led_manager = LedManager(False, board.D18, brightness, num_pixels)
else:
    led_manager = LedManager(True, "D18", brightness, num_pixels)


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


@app.route('/status', methods=['GET'])
def get_status():
    return flask.Response(status=200)


if __name__ == '__main__':
    eureka_client.init_registry_client(eureka_server="http://" + eureka_hostname + ":" + str(eureka_port) + "/eureka",
                                       app_name=app_name,
                                       instance_port=port)

    if start_up_mode == "procedure":
        led_manager.start_procedure(start_up_selection)
    elif start_up_mode == "color":
        led_manager.fill_color("color", False)

    app.run(host=hostname, port=port)
