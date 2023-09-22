import pigpio
import threading
import time

GPIO_MOTOR1 = 12
GPIO_MOTOR2 = 13

MOTOR_PWM_FREQUENCY = 50
MOTOR_MAX_FREQUENCY = 120000
MOTOR_MIN_FREQUENCY = 25000

MIN_PULSEWIDTH = 1200
MAX_PULSEWIDTH = 1800


'''
using set_servo_pulsewidth to move to certain angle,
and get_servo_pulsewidth to get pulsewidth passing to motor.
'''

print("start")
pi = pigpio.pi()
pi.set_mode(GPIO_MOTOR1, pigpio.OUTPUT)
pi.set_mode(GPIO_MOTOR2, pigpio.OUTPUT)

print("pulsewidth at 1500")
pi.set_servo_pulsewidth(GPIO_MOTOR1, 1500)
pi.set_servo_pulsewidth(GPIO_MOTOR2, 1500)
time.sleep(3)

def move(motor, pulsewidth):
    pi.set_servo_pulsewidth(motor, pulsewidth)

def move_with_sleep(motor, pulsewidth):
    pi.set_servo_pulsewidth(motor, pulsewidth)
    time.sleep(0.3)


time.sleep(3)
print('--- move no sleep ---')

for i in range(4):
    
    print("moving to: %s" % (1500 + i * 100))
    start_time = time.time()
    move(GPIO_MOTOR1, 1500 + i * 100)
    move(GPIO_MOTOR2, 1500 + i * 100)
    print("total time: %s" % (time.time() - start_time))


time.sleep(3)
print('--- move with sleep ---')

for i in range(4):
    
    print("moving to: %s" % (1500 + i * 100))
    start_time = time.time()
    move_with_sleep(GPIO_MOTOR1, 1500 + i * 100)
    move_with_sleep(GPIO_MOTOR2, 1500 + i * 100)
    print("total time: %s" % (time.time() - start_time()))


time.sleep(3)
print('--- move with thread ---')

for i in range(4):
    
    t_m1 = threading.Thread(target=move, args=(GPIO_MOTOR1, (1500 + i * 100)))
    t_m2 = threading.Thread(target=move, args=(GPIO_MOTOR2, (1500 + i * 100)))
    print("moving to: %s" % (1500 + i * 100))
    start_time = time.time()
    t_m1.start()
    t_m2.start()
    t_m1.join()
    t_m2.join()
    print("total time: %s" % (time.time() - start_time()))

time.sleep(3)
print('--- move with sleep with thread ---')

for i in range(4):
    
    t_m1 = threading.Thread(target=move_with_sleep, args=(GPIO_MOTOR1, (1500 + i * 100)))
    t_m2 = threading.Thread(target=move_with_sleep, args=(GPIO_MOTOR2, (1500 + i * 100)))
    print("moving to: %s" % (1500 + i * 100))
    start_time = time.time()
    t_m1.start()
    t_m2.start()
    t_m1.join()
    t_m2.join()
    print("total time: %s" % (time.time() - start_time()))


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