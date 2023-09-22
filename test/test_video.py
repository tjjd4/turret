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
    def test_empty_frame(self):
        frame = [0] * (24 * 32) # 24 rows and 32 columns
        temp_range = (30, 40)
        
        processed_matrix, max_temp = VideoUtils.process_frame(frame, temp_range)
        
        self.assertTrue((processed_matrix == 0).all())
        self.assertEqual(max_temp, 0)
        
    def test_frame_with_all_values_in_temp_range(self):
        frame = [35] * (24 * 32) # All values are within the temp_range
        temp_range = (30, 40)
        
        processed_matrix, max_temp = VideoUtils.process_frame(frame, temp_range)
        
        self.assertTrue(np.any(processed_matrix != 0)) # Expecting some non-zero values in the processed_matrix
        self.assertEqual(max_temp, 35) # Max temperature should be 35
    
    def test_frame_with_no_values_in_temp_range(self):
        frame = [25] * (24 * 32) # All values are below the temp_range
        temp_range = (30, 40)
        
        processed_matrix, max_temp = VideoUtils.process_frame(frame, temp_range)
        
        self.assertTrue((processed_matrix == 0).all()) # Expecting all zeros in the processed_matrix
        self.assertEqual(max_temp, 0)
    
    def test_frame_some_values_in_temp_range_fuk(self):
        frame = [20] * (24 * 32) # All values are within the temp_range
        frame = np.array(frame, dtype=np.float32).reshape(24,32)
        assert_matrix = [0] * (24 * 32)
        assert_matrix = np.array(assert_matrix, dtype=np.float32).reshape(24,32)
        for i in range(1,6):
            for j in range(1,4):
                frame[i][j] = 35
                assert_matrix[i][j] = 255
        temp_range = (30, 40)
        
        

        processed_matrix, max_temp = VideoUtils.process_frame(frame, temp_range)
        self.assertEqual(processed_matrix.tolist(), assert_matrix.tolist()) # Expecting some non-zero values in the processed_matrix
        self.assertEqual(max_temp, 35)

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

