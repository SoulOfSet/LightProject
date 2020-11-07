from procedures.procedure import Procedure
import random
import colors
import time


class ChristmasProcedure(Procedure):
    CHRISTMAS_COLORS = [colors.GREEN, colors.RED]

    def __init__(self):
        super(ChristmasProcedure, self).__init__()

    @staticmethod
    def get_name():
        return "christmas"

    def run(self):
        super(ChristmasProcedure, self).run()
        while self.should_stop is False:
            for i in range(self.led_manager.num_pixels):
                pixel_index = random.choice(self.CHRISTMAS_COLORS)
                self.led_manager.set_pixel(i, pixel_index)
            self.led_manager.show_pixels()
            time.sleep(1)

        self.is_running = False
