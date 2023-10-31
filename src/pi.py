import pigpio
import atexit
from src.turret import GPIO_MOTOR1, GPIO_MOTOR2, MOTOR_PULSEWIDTH_MID

class Pi(object):
    def __init__(self):
        self.pi = pigpio.pi()
        atexit.register(self._stop)

    def initialize(self):
        self._setMode(GPIO_MOTOR1, pigpio.OUTPUT)
        self._setMode(GPIO_MOTOR2, pigpio.OUTPUT)

    def calibrate(self):
        self._setServoPulsewidth(GPIO_MOTOR1, MOTOR_PULSEWIDTH_MID)
        self._setServoPulsewidth(GPIO_MOTOR2, MOTOR_PULSEWIDTH_MID)

    def move(self, motor, puslewidth):
        self._setServoPulsewidth(motor, puslewidth)

    def motorOff(self):
        self._write(GPIO_MOTOR1, 0)
        self._write(GPIO_MOTOR2, 0)

    def endConnection(self):
        self._stop()

    def setCallback(self, gpio, func):
        self._callback(gpio, pigpio.FALLING_EDGE, func)

    # functions bellow are provided by pigpio library
    def _setServoPulsewidth(self, gpio, pulsewidth):
        self.pi.set_servo_pulsewidth(gpio, pulsewidth)

    def _stop(self):
        self.pi.stop()

    def _setMode(self, gpio, mode):
        self.pi.set_mode(gpio, mode)

    def _write(self, gpio, level):
        self.pi.write(gpio, level)

    def _callback(self, gpio, edge, func):
        self.pi.callback(gpio, edge, func)