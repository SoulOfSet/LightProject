import board
import flask
from flask import Flask, request
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
    led_manager = LedManager(True, board.D18, 0.75, 100)
else:
    led_manager = LedManager(True, "D18", 0.75, 100)


@app.route('/setcolor', methods=['GET'])
def setcolor():
    color = request.args.get('color')
    is_color = led_manager.fill_color(color)
    if is_color:
        return flask.Response(status=200)
    else:
        return flask.Response(status=500)


@app.route('/setprocedure', methods=['GET'])
def setprocedure():
    procedure = request.args.get('procedure')
    is_real_proc = led_manager.start_procedure(procedure)
    if is_real_proc:
        return flask.Response(status=200)
    else:
        return flask.Response(status=500)


if __name__ == '__main__':
    app.run(host='localhost', port=8080)