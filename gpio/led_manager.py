import time
import colors
from procedures.halloween import HalloweenProcedure
from procedures.procedure import Procedure
from procedures.rainbow import RainbowProcedure

try:
    import neopixel
except ImportError:
    print("No neopixel")


class LedManager:
    pin = None
    debug_mode = False
    brightness = 0
    pixel_order = "GRB"
    num_pixels = 0
    pixels = None
    curr_thread = None
    available_procedures = {}

    def __init__(self, debug_mode, pin, brightness, num_pixels):
        self.debug_mode = debug_mode
        self.pin = pin
        self.brightness = brightness
        self.num_pixels = num_pixels

        for cls in Procedure.__subclasses__():
            self.available_procedures[cls.get_name()] = cls

        if debug_mode is False:
            self.pixels = neopixel.NeoPixel(self.pin, self.num_pixels, brightness=0.5, auto_write=False,
                                            pixel_order=self.pixel_order)

    def fill_color(self, color):
        if colors.COLORS.get(color) is not None:
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
        if procedure in self.available_procedures:
            self.stop_thread_if_running()
            self.curr_thread = self.available_procedures[procedure]()
            self.curr_thread.init(self.pixels, self.num_pixels, self)
            self.curr_thread.start()
            return True
        else:
            return False
