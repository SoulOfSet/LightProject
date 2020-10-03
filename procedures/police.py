import time

from procedures.procedure import Procedure


class PoliceProcedure(Procedure):

    is_red = False

    def __init__(self):
        super(PoliceProcedure, self).__init__()

    @staticmethod
    def get_name():
        return "police"

    def run(self):
        super(PoliceProcedure, self).run()
        while self.should_stop is False:
            if self.is_red:
                self.led_manager.fill_color('blue', False)
            else:
                self.led_manager.fill_color('red', False)
            self.is_red = not self.is_red
            self.led_manager.show_pixels()
            time.sleep(0.2)

        self.is_running = False