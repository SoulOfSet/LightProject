import board
import flask
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
    app.run(host='0.0.0.0', port=8080)
