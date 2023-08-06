import time

import colors
from procedures.procedure import Procedure

try:
    import neopixel
except ImportError:
    print("No neopixel")


class LedManager:
    pin = None
    debug_mode = False
    brightness = 0
    num_pixels = 0
    pixels = None
    curr_thread = None
    pixel_order = None
    available_procedures = {}

    mode = None
    type = None

    def __init__(self, debug_mode, pin, brightness, num_pixels, pixel_order):
        self.debug_mode = debug_mode
        self.pin = pin
        self.brightness = brightness
        self.num_pixels = num_pixels
        self.pixel_order = pixel_order

        for cls in Procedure.__subclasses__():
            self.available_procedures[cls.get_name()] = cls

        if debug_mode is False:
            self.pixels = neopixel.NeoPixel(self.pin, self.num_pixels, brightness=0.5, auto_write=False,
                                            pixel_order=self.pixel_order)

    def fill_color(self, color, stop_current=True):
        mode = "COLOR"
        type = color
        if colors.COLORS.get(color) is not None:
            if stop_current:
                self.stop_thread_if_running()
            if self.debug_mode is True:
                data = "({})".format(','.join(str(p) for p in colors.COLORS[color]))
                print("Filling color : " + color + " " + data)
            else:
                self.pixels.fill(colors.COLORS.get(color))
                self.pixels.show()
            return True
        else:
            return False

    def set_pixel(self, index, color):
        if self.debug_mode is True:
            data = "({})".format(','.join(str(p) for p in color))
            print("Setting pixel : " + str(index) + " to color: " + data)
        else:
            self.pixels[index] = color

    def show_pixels(self):
        if self.debug_mode is False:
            self.pixels.show()
        else:
            print("Filling pixels")

    def stop_thread_if_running(self):
        if self.curr_thread is not None:
            if self.curr_thread.is_running is True:
                self.curr_thread.stopit()
                self.curr_thread.join()
                time.sleep(1)
                self.curr_thread = None

    def start_procedure(self, procedure):
        mode = "PROCEDURE"
        type = procedure.get_name()
        if procedure in self.available_procedures:
            self.stop_thread_if_running()
            self.curr_thread = self.available_procedures[procedure]()
            self.curr_thread.init(self)
            self.curr_thread.start()
            return True
        else:
            return False

    def get_procedures(self):
        return self.available_procedures.keys()

    def get_mode(self):
        return self.mode

    def get_type(self):
        return self.type
