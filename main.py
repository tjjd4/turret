import cv2
import sys
import board
import busio
import atexit
import threading
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

# using pulsewidth to control motor spin to a specific angle
# using set_servo_pulsewidth to move to certain angle,
# and get_servo_pulsewidth to get the signal pulsewidth passing to motor.

MOTOR_PULSEWIDTH_MIN = 1000
MOTOR_PULSEWIDTH_MID = 1500
MOTOR_PULSEWIDTH_MAX = 1900

# not using pi.hardware_PWM() to control the motor, using pi.set_servo_pulsewidth() instead.
# 
# MOTOR_PWM_FREQUENCY = 50
# MOTOR_PWM_DUTY_CYCLE_180 = 120000
# MOTOR_PWM_DUTY_CYCLE_90 = 60000
# MOTOR_PWM_DUTY_CYCLE_0 = 20000
# MOTOR_PWM_RANGE = 400

'''
MLX90640-BAA IR Thermal Camera

I2C compatible digital interface
Programmable refresh rate 0.5Hz…64Hz (0.25 ~ 32 FPS)
3.3V-5V supply voltage, regulated to 3.3V on breakout
Current consumption less than 23mA
Field of view: 110°x75°
Operating temperature -40°C ~ 85°C
Target temperature -40°C ~ 300°C
Product Dimensions: 25.8mm x 17.8mm x 10.5mm / 1.0" x 0.7" x 0.4"
Product Weight: 3.0g / 0.1oz 
'''
IMAGE_CENTER_POINT_X = 15
IMAGE_CENTER_POINT_Y = 11


class VideoUtils(object):
    '''
    Class used for video processing
    '''
    @staticmethod
    def trackHeat():
        i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

        mlx = adafruit_mlx90640.MLX90640(i2c)
        print("MLX addr detected on I2C", [hex(i) for i in mlx.serial_number])

        # if using higher refresh rates yields a 'too many retries' exception,
        # try decreasing this value to work with certain pi/camera combinations
        mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

        frame = [0] * 768
        while True:
            try:
                mlx.getFrame(frame)
            except ValueError:
                # these happen, no biggie - retry
                continue

            thermal_matrix =np.array(frame).reshape(24, 32)
            highest_temp = thermal_matrix.max()
            thermal_matrix[thermal_matrix != highest_temp] = 0

            for h in range(24):
                for w in range(32):
                    t = frame[h*32 + w]
                    print("%0.1f, " % t, end="")
                print()
            print()





class Turret(object):
    '''
    Class used for turret control
    control a turret with two servo motor
    '''
    def __init__(self):
        logging.getLogger().setLevel(logging.DEBUG)
        logging.info('Turret Start initialize')
        self.pi = pigpio.pi()
        self.pi.set_mode(GPIO_MOTOR1, pigpio.OUTPUT)
        self.pi.set_mode(GPIO_MOTOR2, pigpio.OUTPUT)
        # self.pi.set_PWM_frequency(GPIO_MOTOR1, MOTOR_PWM_FREQUENCY)
        # self.pi.set_PWM_range(GPIO_MOTOR1, MOTOR_PWM_RANGE)
        # self.pi.set_PWM_frequency(GPIO_MOTOR2, MOTOR_PWM_FREQUENCY)
        # self.pi.set_PWM_range(GPIO_MOTOR2, MOTOR_PWM_RANGE)

        # set to relocate and release the motors
        atexit.register(self.__turn_of_motors)
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

        
        if x > 0:
            if self.m1_pulsewidth < MOTOR_PULSEWIDTH_MAX:
                self.m1_pulsewidth = self.m1_pulsewidth + 100
                t_m1 = threading.Thread(target=self.__move, args=(GPIO_MOTOR1, self.m1_pulsewidth))
        elif x < 0:
            if self.m1_pulsewidth > MOTOR_PULSEWIDTH_MID:
                self.m1_pulsewidth = self.m1_pulsewidth - 100
                t_m1 = threading.Thread(target=self.__move, args=(GPIO_MOTOR1, self.m1_pulsewidth))
        
        if y > 0:
            if self.m2_pulsewidth < MOTOR_PULSEWIDTH_MAX:
                self.m2_pulsewidth = self.m2_pulsewidth + 100
                t_m2 = threading.Thread(target=self.__move, args=(GPIO_MOTOR2, self.m2_pulsewidth))
        elif y < 0:
            if self.m2_pulsewidth > MOTOR_PULSEWIDTH_MID:
                self.m2_pulsewidth = self.m2_pulsewidth - 100
                t_m2 = threading.Thread(target=self.__move, args=(GPIO_MOTOR2, self.m2_pulsewidth))

        # starting thread (controlling motor)
        t_m1.start()
        t_m2.start()

        # wait until thread end
        t_m1.join()
        t_m2.join()
    
    def __move(self, motor, puslewidth):
        self.pi.set_servo_pulsewidth(motor, puslewidth)


    # start thermal detection
    def thermal_detection(self):
        return
    
    def move(self, frame):
        h, w = frame.shape[:2]

    def __turn_of_motors(self):
        self.calibrate()
        self.pi.write(GPIO_MOTOR1, 0)
        self.pi.write(GPIO_MOTOR2, 0)
        self.pi.stop()

if __name__ == '__main__':

    print('program activate')
    print('-----------------')
    t = Turret()
    t.calibrate()
    t.thermal_detection()
