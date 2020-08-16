import board
import flask
import neopixel
from flask import Flask, request

from procedures import *

# Create Flask object called app.
app = Flask(__name__)

pixel_pin = board.D18
num_pixels = 50
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER)
curr_thread = None


def stop_thread_if_running():
    global curr_thread
    if curr_thread is not None:
        if curr_thread.is_running is True:
            curr_thread.stopit()
            curr_thread.join()
            time.sleep(1)
            curr_thread = None


@app.route('/setcolor', methods=['GET'])
def setcolor():
    color = request.args.get('color')
    if colors.COLORS.get(color) != None:
        stop_thread_if_running()
        pixels.fill(colors.COLORS.get(color))
        pixels.show()
        return flask.Response(status=200)
    else:
        return flask.Response(status=500)


@app.route('/setprocedure', methods=['GET'])
def setprocedure():
    procedure = request.args.get('procedure')
    is_real_proc = start_procedure(procedure)

    if is_real_proc:
        return flask.Response(status=200)
    else:
        return flask.Response(status=500)


def start_procedure(procedure):
    global curr_thread
    stop_thread_if_running()

    if procedure == "halloween":
        curr_thread = HalloweenProcedure()
        curr_thread.init(pixels, num_pixels)
        curr_thread.start()
        return True
    elif procedure == "rainbow":
        curr_thread = RainbowProcedure()
        curr_thread.init(pixels, num_pixels)
        curr_thread.start()
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(host='192.168.1.8', port=8080)