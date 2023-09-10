import cv2
import sys
import board
import busio
import atexit
import logging
import pigpio
import numpy as np
import adafruit_mlx90640

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
MOTOR_PWM_FREQUENCY = 50
MOTOR_PWM_RANGE = 400

'''
Class used for video processing
'''
class VideoUtils(object):

    def process_thermal_video(self, camera_port = 0):
        camera = cv2.VideoCapture(camera_port)
        
        while True:
            ret, frame = camera.read()

            if not ret:
                logging.warning('--- Camera Error ---')
                break     




"""
Class used for turret control
control a turret with two servo motor
"""
class Turret(object):

    def __init__(self):
        logging.getLogger().setLevel(logging.DEBUG)
        logging.info('Start initialize')
        self.pi = pigpio.pi()
        self.pi.set_mode(GPIO_MOTOR1, pigpio.OUTPUT)
        self.pi.set_mode(GPIO_MOTOR2, pigpio.OUTPUT)
        self.pi.set_PWM_frequency(GPIO_MOTOR1, MOTOR_PWM_FREQUENCY)
        self.pi.set_PWM_range(GPIO_MOTOR1, MOTOR_PWM_RANGE)
        self.pi.set_PWM_frequency(GPIO_MOTOR2, MOTOR_PWM_FREQUENCY)
        self.pi.set_PWM_range(GPIO_MOTOR2, MOTOR_PWM_RANGE)

        # set to relocate and release the motors
        atexit.register(self.__turn_of_motors)
        logging.info('Initialize sucess')

    # calibrate two servo motors to central position
    def calibrate(self):
        logging.debug('Start calibrate')
        self.pi.hardware_PWM(GPIO_MOTOR1, MOTOR_PWM_FREQUENCY, 500000)
        self.pi.hardware_PWM(GPIO_MOTOR2, MOTOR_PWM_FREQUENCY, 500000)
        logging.debug('Calibrate success')

    # start thermal detection
    def thermal_detection(self):
        return

    def __turn_of_motors(self):
        self.pi.hardware_PWM(GPIO_MOTOR1, MOTOR_PWM_FREQUENCY, 500000)
        self.pi.hardware_PWM(GPIO_MOTOR2, MOTOR_PWM_FREQUENCY, 250000)
        self.pi.write(GPIO_MOTOR1, 0)
        self.pi.write(GPIO_MOTOR2, 0)
        self.pi.stop()

# if __name__ == '__main__':