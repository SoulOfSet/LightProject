import time

from procedures.procedure import Procedure


class RainbowProcedure(Procedure):
    def __init__(self):
        super(RainbowProcedure, self).__init__()

    def wheel(self, pos):
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return r, g, b

    @staticmethod
    def get_name():
        return "rainbow"

    def run(self):
        super(RainbowProcedure, self).run()
        while self.should_stop is False:
            for j in range(255):
                for i in range(self.led_manager.num_pixels):
                    pixel_index = (i * 256 // self.led_manager.num_pixels) + j
                    self.led_manager.set_pixel(i, self.wheel(pixel_index & 255))
                self.led_manager.show_pixels()
                time.sleep(0.001)

        self.is_running = False
