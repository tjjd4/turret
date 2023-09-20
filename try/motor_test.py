import pigpio
import time

GPIO_MOTOR1 = 12
GPIO_MOTOR2 = 13
GPIO_MOTOR1_FEEDBACK = 18

MOTOR_PWM_FREQUENCY = 50
MOTOR_MAX_FREQUENCY = 120000
MOTOR_MIN_FREQUENCY = 25000

MIN_PULSEWIDTH = 1000
MAX_PULSEWIDTH = 2000


'''
using set_servo_pulsewidth to move to certain angle,
and get_servo_pulsewidth to get pulsewidth passing to motor.
'''

print("start")
pi = pigpio.pi()
pi.set_mode(GPIO_MOTOR1, pigpio.OUTPUT)

# initial_pulsewidth = 1000
# for i in range(21):
#     print( "working at:" + str(initial_pulsewidth))
#     pi.set_servo_pulsewidth(12, initial_pulsewidth)
#     print(pi.get_servo_pulsewidth(12))
#     time.sleep(1)
#     initial_pulsewidth += 50
#     try:
#         print(pi.get_servo_pulsewidth(6))
#     except:
#         continue
print("pulsewidth at 1500")
pi.set_servo_pulsewidth(12, 1500)
time.sleep(3)

for i in range(4):
    pi.set_servo_pulsewidth(12, 1500 + i * 100)
pi.write(GPIO_MOTOR1, 0)
pi.write(GPIO_MOTOR2, 0)
pi.stop()

print("-------end------")



'''
using `set_servo_pulsewidth()` can locate the motor spin to different position (angle),
since `hardware_PWM()` can only control the rotation.
Or i don't know how to

Motor: K-Power Hb200t 12V 200kg Torque Steel Gear Digital Industrial Servo
'''
# pi.hardware_PWM(GPIO_MOTOR1, MOTOR_PWM_FREQUENCY, 30000)
# time.sleep(5)
# 
# start_time = time.time()
# print("frequency at 120000")
# pi.hardware_PWM(GPIO_MOTOR1, MOTOR_PWM_FREQUENCY, 120000)
# time.sleep(5)
# 
# print("totally close to move : %s seconds ---" % (time.time() - start_time))