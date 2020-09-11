from procedures.procedure import Procedure
import random
import colors
import time


class HalloweenProcedure(Procedure):
    HALLOW_COLORS = [colors.GREEN, colors.PURPLE, colors.ORANGE]

    def __init__(self):
        super(HalloweenProcedure, self).__init__()

    @staticmethod
    def get_name():
        return "halloween"

    def run(self):
        super(HalloweenProcedure, self).run()
        while self.should_stop is False:
            for i in range(self.led_manager.num_pixels):
                pixel_index = random.choice(self.HALLOW_COLORS)
                self.led_manager.set_pixel(i, pixel_index)
            self.led_manager.show_pixels()
            time.sleep(1)

        self.is_running = False
