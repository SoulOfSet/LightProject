import threading
import time

class Procedure(threading.Thread):

    pixels = None
    should_stop = False
    is_running = False
    num_pixels = 0

    def __init__(self, *args, **kwargs):
        super(Procedure, self).__init__(*args, **kwargs)

    def init(self, pixels, num_pixels):
       self.pixels = pixels
       self.num_pixels = num_pixels

    def run(self):
        self.is_running = True

    def stopit(self):
        self.should_stop = True
