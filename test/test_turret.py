import unittest
from src.turret import Turret
from src.turret import GPIO_MOTOR1, GPIO_MOTOR2, MOTOR_PULSEWIDTH_MID

class TurretTestCase(unittest.TestCase):
    def test_init(self):
        t = Turret()
        self.assertIsNotNone(t.pi)
        self.assertEqual(t.temp_range[0], 30)
        self.assertEqual(t.temp_range[1], 40)
        self.assertEqual(t.pi.get_mode(GPIO_MOTOR1), 1)
        self.assertEqual(t.pi.get_mode(GPIO_MOTOR2), 1)

        temp_range = (50, 60)
        t = Turret(temp_range)
        self.assertEqual(t.temp_range[0], 50)
        self.assertEqual(t.temp_range[1], 60)

    def test_calibrate(self):
        t = Turret()
        t.calibrate()
        self.assertEqual(t.m1_pulsewidth, MOTOR_PULSEWIDTH_MID)
        self.assertEqual(t.m2_pulsewidth, MOTOR_PULSEWIDTH_MID)
        self.assertEqual(t.pi.get_servo_pulsewidth(GPIO_MOTOR1), MOTOR_PULSEWIDTH_MID)
        self.assertEqual(t.pi.get_servo_pulsewidth(GPIO_MOTOR2), MOTOR_PULSEWIDTH_MID)

    def test_track(self):
        t = Turret()
        t.calibrate()
        t.track(1, 1)
        self.assertEqual(t.m1_pulsewidth, MOTOR_PULSEWIDTH_MID + 25)
        self.assertEqual(t.m2_pulsewidth, MOTOR_PULSEWIDTH_MID + 25)
        t.track(-1, -1)
        self.assertEqual(t.m1_pulsewidth, MOTOR_PULSEWIDTH_MID)
        self.assertEqual(t.m2_pulsewidth, MOTOR_PULSEWIDTH_MID)
        t.track(1, -1)
        self.assertEqual(t.m1_pulsewidth, MOTOR_PULSEWIDTH_MID + 25)
        self.assertEqual(t.m2_pulsewidth, MOTOR_PULSEWIDTH_MID - 25)
        t.track(-1, 1)
        self.assertEqual(t.m1_pulsewidth, MOTOR_PULSEWIDTH_MID)
        self.assertEqual(t.m2_pulsewidth, MOTOR_PULSEWIDTH_MID)

    def test___move(self):
        t = Turret()
        t.calibrate()
        t.__move(GPIO_MOTOR1, MOTOR_PULSEWIDTH_MID + 25)
        self.assertEqual(t.pi.get_servo_pulsewidth(GPIO_MOTOR1), MOTOR_PULSEWIDTH_MID + 25)
        t.__move(GPIO_MOTOR2, MOTOR_PULSEWIDTH_MID - 25)
        self.assertEqual(t.pi.get_servo_pulsewidth(GPIO_MOTOR2), MOTOR_PULSEWIDTH_MID - 25)

    def test___turn_off_motors(self):
        t = Turret()
        t.calibrate()
        t.__turn_off_motors()
        with self.assertRaises():
            t.pi.get_servo_pulsewidth(GPIO_MOTOR1)

        with self.assertRaises():
            t.pi.get_servo_pulsewidth(GPIO_MOTOR2)

    def setUp(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()