import threading


class Procedure(threading.Thread):
    should_stop = False
    is_running = False
    led_manager = None

    def __init__(self, *args, **kwargs):
        super(Procedure, self).__init__(*args, **kwargs)

    def init(self, led_manager):
        self.led_manager = led_manager

    @staticmethod
    def get_name():
        return "NO_PROC"

    #TODO: Add optional extra arguments for more complex procedures without writing....whole new ones
    def run(self):
        self.is_running = True

    def stopit(self):
        self.should_stop = True
