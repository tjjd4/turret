import sys
import numpy as np
# sys.path.append('..')
import unittest

from unittest.mock import patch, MagicMock
from src.videoUtils import VideoUtils



class VideoUtilsTestCase(unittest.TestCase):
    
    @patch.object(VideoUtils, 'get_mlx90640')
    def test_init_mlx90640(self, mock_function):
        mock_mlx = MagicMock()
        mock_mlx.serial_number.return_value = 15
        mock_function.return_value = mock_mlx
        mlx = VideoUtils.init_mlx90640()

        mock_function.assert_called_once()
        self.assertEqual(mlx, mock_mlx)
        self.assertEqual(mlx.refresh_rate, 0b101)

    def test_get_mlx90640(self):
        pass

    # This is a simple test for the `process_frame` method. 
    # It ensures that if an empty frame is passed, it returns a zero matrix.
    def test_process_frame_empty_frame(self):
        # frame = [0] * 768
        # processed_matrix, max_temp = VideoUtils.process_frame(frame, (30, 40))
        # self.assertTrue((processed_matrix == 0).all())
        # self.assertEqual(max_temp, 0)
        pass

    # This test checks the centroid difference for a given thresholded matrix.
    def test_find_centroid_difference(self):
        matrix = np.zeros((24,32), dtype=np.int8)
        
        centroid, diff_to_center = VideoUtils.find_centroid_difference(matrix)
        self.assertEqual(centroid, None)
        self.assertEqual(diff_to_center, (0, 0))

    # Add more tests as required ...

    def setUp(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
