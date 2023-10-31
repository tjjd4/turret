from simple_pid import PID

class Pid(object):
    def __init__(self):
        self.pid = PID(1, 0.1, 0.05, setpoint=0, output_limits=(0, 100))

    def calculateMove(self, value):
        output = self.pid(abs(value))