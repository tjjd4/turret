import pigpio
import atexit

class Pi(object):
    def __init__(self):
        self.pi = pigpio.pi()

    def setServoPulsewidth(self, motor, pulsewidth):
        self.pi.set_servo_pulsewidth(motor, pulsewidth)

    def stop(self):
        self.pi.stop()