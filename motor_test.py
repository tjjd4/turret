import pigpio
import time

GPIO_MOTOR1 = 12
GPIO_MOTOR2 = 13
GPIO_MOTOR1_FEEDBACK = 18

MOTOR_PWM_FREQUENCY = 50

print("start")
pi = pigpio.pi()
pi.set_mode(GPIO_MOTOR1, pigpio.OUTPUT)

print("frequency at 500000")

pi.hardware_PWM(GPIO_MOTOR1, MOTOR_PWM_FREQUENCY, 500000)
time.sleep(1)
start_time = time.time()
pi.write(GPIO_MOTOR1, 0)
pi.hardware_PWM(GPIO_MOTOR1, MOTOR_PWM_FREQUENCY, 750000)
print("totally close to move : %s seconds ---" % (time.time() - start_time))
time.sleep(1)
start_time = time.time()
pi.hardware_PWM(GPIO_MOTOR1, MOTOR_PWM_FREQUENCY, 500000)
pi.hardware_PWM(GPIO_MOTOR1, MOTOR_PWM_FREQUENCY, 250000)
print("stop freq to move : %s seconds ---" % (time.time() - start_time))

pi.write(GPIO_MOTOR1, 0)
pi.write(GPIO_MOTOR2, 0)
pi.stop()

print("-------end------")