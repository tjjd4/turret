import unittest
from unittest.mock import patch, Mock
from main import VideoUtils, Turret

class VideoUtilsToTurretTestCase(unittest.TestCase):

    @patch('main.adafruit_mlx90640.MLX90640', autospec=True)
    @patch.object(Turret, 'track')
    @patch('main.busio.I2C', autospec=True)
    @patch('main.pigpio.pi', autospec=True)
    @patch('main.board', autospec=True)
    @patch('main.time.sleep', autospec=True)  # Mock sleep to speed up the test
    def test_thermal_detection_interaction_with_turret(self, mock_sleep, mock_board, mock_pi, mock_i2c, mock_track, MockMLX90640):
        # Setup
        mlx_mock = MockMLX90640.return_value
        frame = [0] * 768  # An empty frame for simplicity
        mlx_mock.getFrame.return_value = frame

        # Instantiate the turret and call the thermal_detection method
        turret = Turret()
        VideoUtils.thermal_detection(turret.track, (30, 40))

        # Assertions
        mock_track.assert_called()  # Ensure that turret.track was called

    def setUp(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()

