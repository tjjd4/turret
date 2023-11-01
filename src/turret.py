import atexit
import time
import threading
import logging
import multiprocessing
from simple_pid import PID
from src.videoUtils import VideoUtils
from src.pi import Pi

'''
Raspberry Pi 4 Model B
Pins with hardware PWM:
channel 0:
    GPIO 12
    GPIO 18
channel 1:
    GPIO 13
    GPIO 19
'''
GPIO_MOTOR1 = 12
GPIO_MOTOR2 = 13

'''
K-Power Hb200t 12V 200kg Torque Steel Gear Digital Industrial Servo

Voltage Range	        DC 10-14.8V
Rated Voltage	        12V
Stall Torque	        20.1N.M(205kg.cm)
No load Speed	        55.5rpm(0.18s/60°)
Motor Type	            Brushless
Resolution	            0.23°
Running Degree	        0-180°
Communication Method	PWM(deadband 1-2μs)
NO.of Wire	5Pin
Position Sensor	        Potentiometer
'''

# using pulsewidth to control motor spin to a specific angle
# using set_servo_pulsewidth to move to certain angle,
# and get_servo_pulsewidth to get the signal pulsewidth passing to motor.

MOTOR_PULSEWIDTH_MIN = 1200
MOTOR_PULSEWIDTH_MID = 1500
MOTOR_PULSEWIDTH_MAX = 1800

# not using pi.hardware_PWM() to control the motor, using pi.set_servo_pulsewidth() instead.
# 
# MOTOR_PWM_FREQUENCY = 50
# MOTOR_PWM_DUTY_CYCLE_180 = 120000
# MOTOR_PWM_DUTY_CYCLE_90 = 60000
# MOTOR_PWM_DUTY_CYCLE_0 = 20000
# MOTOR_PWM_RANGE = 400

'''
Class used for turret control
control a turret with two servo motor
'''
TURRET_PENDING = 0
TURRET_OFF = -1
TURRET_RUNNING = 1

class Turret(object):
    
    def __init__(self, temp_range = (50, 300), pi4=None):
        logging.info('Turret Start initialize')

        self.status = TURRET_OFF

        self.pid = PID(1, 0.1, 0.05, setpoint=0)
        self.pid.sample_time = 1.0 / 16
        # initialize raspberry pi connection
        self.initial_setup(temp_range, pi4)

        # set to relocate and release the motors
        atexit.register(self.off)

    def initial_setup(self, temp_range = (50, 300), pi4 = None):
        if self.status == TURRET_OFF:
            self.temp_range = temp_range
            if pi4 == None:
                pi4 = Pi()
            self.pi4 = pi4
            self.pi4.initialize()
            self.status = TURRET_PENDING
            logging.info('Turret Initialize sucess')
        else:
            logging.warning("---------turret is not off !!!---------")
        

    # calibrate two servo motors to central position
    def calibrate(self):
        logging.debug('Start calibrate')
        self.pi4.calibrate()
        self.m1_pulsewidth = MOTOR_PULSEWIDTH_MID
        self.m2_pulsewidth = MOTOR_PULSEWIDTH_MID
        logging.debug('Calibrate success')

    def track(self, x, y):
        
        t_m1 = threading.Thread()
        t_m2 = threading.Thread()

        # motor1_pulsewidth_now = self.pi.get_servo_pulsewidth(GPIO_MOTOR1)
        # motor2_pulsewidth_now = self.pi.get_servo_pulsewidth(GPIO_MOTOR2)
        # logging.debug("motor1 pulsewidth now: %s" % (motor1_pulsewidth_now))
        # logging.debug("motor2 pulsewidth now: %s" % (motor2_pulsewidth_now))

        if x > 1:
            if self.m2_pulsewidth >= MOTOR_PULSEWIDTH_MID and self.m1_pulsewidth > MOTOR_PULSEWIDTH_MIN:
                self.m1_pulsewidth = self.m1_pulsewidth - 25
                t_m1 = threading.Thread(target=self.__move, args=(GPIO_MOTOR1, self.m1_pulsewidth))
            elif self.m2_pulsewidth < MOTOR_PULSEWIDTH_MID and self.m1_pulsewidth < MOTOR_PULSEWIDTH_MAX:
                self.m1_pulsewidth = self.m1_pulsewidth + 25
                t_m1 = threading.Thread(target=self.__move, args=(GPIO_MOTOR1, self.m1_pulsewidth))
        elif x < -1:
            if self.m2_pulsewidth >= MOTOR_PULSEWIDTH_MID and self.m1_pulsewidth < MOTOR_PULSEWIDTH_MAX:
                self.m1_pulsewidth = self.m1_pulsewidth + 25
                t_m1 = threading.Thread(target=self.__move, args=(GPIO_MOTOR1, self.m1_pulsewidth))
            elif self.m2_pulsewidth < MOTOR_PULSEWIDTH_MID and self.m1_pulsewidth > MOTOR_PULSEWIDTH_MIN:
                self.m1_pulsewidth = self.m1_pulsewidth - 25
                t_m1 = threading.Thread(target=self.__move, args=(GPIO_MOTOR1, self.m1_pulsewidth))
        
        if y > 1:
            if self.m2_pulsewidth > MOTOR_PULSEWIDTH_MIN:
                self.m2_pulsewidth = self.m2_pulsewidth - 25
                t_m2 = threading.Thread(target=self.__move, args=(GPIO_MOTOR2, self.m2_pulsewidth))
        elif y < -1:
            if self.m2_pulsewidth < MOTOR_PULSEWIDTH_MAX:
                self.m2_pulsewidth = self.m2_pulsewidth + 25
                t_m2 = threading.Thread(target=self.__move, args=(GPIO_MOTOR2, self.m2_pulsewidth))

        # starting thread (controlling motor)
        t_m1.start()
        t_m2.start()

        # wait until thread end
        t_m1.join()
        t_m2.join()
    
    def __move(self, motor, puslewidth):
        logging.debug("-------------move---------------")
        self.pi4.move(motor, puslewidth)


    # start thermal detection
    def start(self, pi4=None, *args):
        if self.status == TURRET_PENDING:
            self.status = TURRET_RUNNING
            self.m_thermal_detection = multiprocessing.Process(target=VideoUtils.thermal_detection, args=(self.track, self.temp_range))
            self.m_thermal_detection.daemon = True
            self.m_thermal_detection.start()
        elif self.status == TURRET_OFF:
            self.initial_setup(self.temp_range, pi4)
            self.start()
        else:
            logging.warning("---------turret is running !!!---------")

    def stop(self, *args):
        if self.status == TURRET_RUNNING:
            self.status = TURRET_PENDING
            self.m_thermal_detection.terminate()
        else:
            logging.warning("---------turret is not running !!!---------")
    
    def off(self):
        if self.status == TURRET_RUNNING:
            self.status = TURRET_PENDING
            self.m_thermal_detection.terminate()

        if self.status != TURRET_OFF:
            self.calibrate()
            time.sleep(0.5)
            self.pi4.motorOff()
            self.pi4.endConnection()

        self.status = TURRET_OFF