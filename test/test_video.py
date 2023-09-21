import sys
sys.path.append('..')
import unittest
from unittest.mock import MagicMock
from src.videoUtils import VideoUtils
try:
    import board
    import busio
    # ... other hardware-specific imports
except (ImportError, NotImplementedError):
    pass

class VideoUtilsTestCase(unittest.TestCase):


    def test_init_mlx90640(self, MockMLX90640):
        mock_i2c = MagicMock()
        mock_mlx = MagicMock()
        mock_i2c.return_value = mock_mlx

        with unittest.mock.patch('busio.I2C', mock_i2c, 'adafruit_mlx90640.MLX90640', mock_mlx):
            mlx = VideoUtils.init_mlx90640()

        mock_mlx.init_mlx90640.assert_called_once_with(board.SCL, board.SDA, frequency=1000000)
        mock_mlx.refresh_rate = MagicMock()
        self.assertEqual(mlx, mock_mlx)

    # # This is a simple test for the `process_frame` method. 
    # # It ensures that if an empty frame is passed, it returns a zero matrix.
    # def test_process_frame_empty_frame(self):
    #     frame = [0] * 768
    #     processed_matrix, max_temp = VideoUtils.process_frame(frame, (30, 40))
    #     self.assertTrue((processed_matrix == 0).all())
    #     self.assertEqual(max_temp, 0)

    # # This test checks the centroid difference for a given thresholded matrix.
    # def test_find_centroid_difference(self):
    #     matrix = [
    #         [0, 0, 0, 0, 0],
    #         [0, 255, 255, 255, 0],
    #         [0, 255, 0, 255, 0],
    #         [0, 255, 255, 255, 0],
    #         [0, 0, 0, 0, 0]
    #     ]
    #     centroid, diff_to_center = VideoUtils.find_centroid_difference(matrix)
    #     self.assertEqual(centroid, (2, 2))
    #     self.assertEqual(diff_to_center, (-13, -9))

    # Add more tests as required ...

    def setUp(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
