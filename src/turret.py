import atexit
import threading
import logging
import pigpio
from src.videoUtils import VideoUtils

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

class Turret(object):
    '''
    Class used for turret control
    control a turret with two servo motor
    '''
    def __init__(self, temp_range = (30, 40)):
        logging.info('Turret Start initialize')

        self.temp_range = temp_range

        # initialize raspberry pi connection
        self.pi = pigpio.pi()
        self.pi.set_mode(GPIO_MOTOR1, pigpio.OUTPUT)
        self.pi.set_mode(GPIO_MOTOR2, pigpio.OUTPUT)
        # self.pi.set_PWM_frequency(GPIO_MOTOR1, MOTOR_PWM_FREQUENCY)
        # self.pi.set_PWM_range(GPIO_MOTOR1, MOTOR_PWM_RANGE)
        # self.pi.set_PWM_frequency(GPIO_MOTOR2, MOTOR_PWM_FREQUENCY)
        # self.pi.set_PWM_range(GPIO_MOTOR2, MOTOR_PWM_RANGE)


        # set to relocate and release the motors
        atexit.register(self.__turn_off_motors)
        logging.info('Turret Initialize sucess')

    # calibrate two servo motors to central position
    def calibrate(self):
        logging.debug('Start calibrate')
        self.pi.set_servo_pulsewidth(GPIO_MOTOR1, MOTOR_PULSEWIDTH_MID)
        self.pi.set_servo_pulsewidth(GPIO_MOTOR2, MOTOR_PULSEWIDTH_MID)
        self.m1_pulsewidth = MOTOR_PULSEWIDTH_MID
        self.m2_pulsewidth = MOTOR_PULSEWIDTH_MID
        logging.debug('Calibrate success')

    def track(self, x, y):
        
        t_m1 = threading.Thread()
        t_m2 = threading.Thread()

        motor1_pulsewidth_now = self.pi.get_servo_pulsewidth(GPIO_MOTOR1)
        motor2_pulsewidth_now = self.pi.get_servo_pulsewidth(GPIO_MOTOR2)
        logging.debug("motor1 pulsewidth now: %s" % (motor1_pulsewidth_now))
        logging.debug("motor2 pulsewidth now: %s" % (motor2_pulsewidth_now))

        if x > 1:
            if y >= 0:
                if self.m1_pulsewidth > MOTOR_PULSEWIDTH_MIN:
                    logging.debug("motor1 - pulsewidth")
                    self.m1_pulsewidth = self.m1_pulsewidth - 25
                    t_m1 = threading.Thread(target=self.__move, args=(GPIO_MOTOR1, self.m1_pulsewidth))
            if y < 0:
                if self.m1_pulsewidth < MOTOR_PULSEWIDTH_MAX:
                    logging.debug("motor1 + pulsewidth")
                    self.m1_pulsewidth = self.m1_pulsewidth + 25
                    t_m1 = threading.Thread(target=self.__move, args=(GPIO_MOTOR1, self.m1_pulsewidth))
        elif x < -1:
            if y >= 0:
                if self.m1_pulsewidth < MOTOR_PULSEWIDTH_MAX:
                    logging.debug("motor1 + pulsewidth")
                    self.m1_pulsewidth = self.m1_pulsewidth + 25
                    t_m1 = threading.Thread(target=self.__move, args=(GPIO_MOTOR1, self.m1_pulsewidth))
            if y < 0:
                if self.m1_pulsewidth > MOTOR_PULSEWIDTH_MIN:
                    logging.debug("motor1 - pulsewidth")
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
        self.pi.set_servo_pulsewidth(motor, puslewidth)


    # start thermal detection
    def thermal_tracking(self):
        VideoUtils.thermal_detection(self.track, self.temp_range)
    

    def __turn_off_motors(self):
        self.calibrate()
        self.pi.write(GPIO_MOTOR1, 0)
        self.pi.write(GPIO_MOTOR2, 0)
        self.pi.stop()