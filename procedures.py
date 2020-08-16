from procedure import Procedure
import random
import colors
import time

class HalloweenProcedure(Procedure):

    HALLOW_COLORS = [colors.GREEN, colors.PURPLE, colors.ORANGE]

    def __init__(self):
        super(HalloweenProcedure,self).__init__()

    def run(self):
        super(HalloweenProcedure,self).run()
        while self.should_stop is False:
            for i in range(self.num_pixels):
                pixel_index = random.choice(self.HALLOW_COLORS)
                self.pixels[i] = pixel_index
            self.pixels.show()
            time.sleep(1)

        self.is_running = False



class RainbowProcedure(Procedure):
    def __init__(self):
        super(RainbowProcedure,self).__init__()

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
        return (r, g, b)

    def run(self):
        super(RainbowProcedure,self).run()
        while self.should_stop is False:
            for j in range(255):
                for i in range(self.num_pixels):
                    pixel_index = (i * 256 // self.num_pixels) + j
                    self.pixels[i] = self.wheel(pixel_index & 255)
                self.pixels.show()
                time.sleep(0.001)

        self.is_running = False