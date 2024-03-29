import os
import board
import flask
import yaml
from flask import Flask, request, jsonify

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
hostname = port = app_name = brightness = start_up_mode = start_up_selection = \
    num_pixels = pixel_order = None

try:
    with open(config_dir + os.sep + "config.yml") as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        hostname = config['hostname']
        port = config['port']
        app_name = config['app_name']
        num_pixels = config['num_pixels']
        brightness = config['brightness']
        start_up_mode = config['start_up_mode']
        start_up_selection = config['start_up_selection']
        pixel_order = config['pixel_order']
except Exception as e:
    print("Unable to load config file")
    print(e)
    exit(1)

curr_thread = None

if is_neopixel:
    led_manager = LedManager(False, board.D18, brightness, num_pixels, pixel_order)
else:
    led_manager = LedManager(True, "D18", brightness, num_pixels, pixel_order)


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
    return jsonify({
        "mode": led_manager.get_mode(),
        "type": led_manager.get_type()
    })

if __name__ == '__main__':

    if start_up_mode == "procedure":
        led_manager.start_procedure(start_up_selection)
    elif start_up_mode == "color":
        led_manager.fill_color("color", False)

    app.run(host=hostname, port=port)