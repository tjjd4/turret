import pigpio
import atexit

class Pi(object):
    def __init__(self):
        self.pi = pigpio.pi()
        atexit.register(self.stop())

    def setServoPulsewidth(self, gpio, pulsewidth):
        self.pi.set_servo_pulsewidth(gpio, pulsewidth)

    def stop(self):
        self.pi.stop()

    def setMode(self, gpio, mode):
        self.pi.set_mode(gpio, mode)

    def write(self, gpio, level):
        self.pi.write(gpio, level)