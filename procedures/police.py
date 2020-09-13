from procedures.procedure import Procedure
import random
import colors
import time


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
                self.led_manager.fill_color(colors.BLUE)
            else:
                self.led_manager.fill_color(colors.RED)
            self.is_red = not self.is_red
            self.led_manager.show_pixels()
            time.sleep(0.5)

        self.is_running = False