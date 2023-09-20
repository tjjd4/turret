import cv2
import time
import board
import busio
import logging
import numpy as np
import adafruit_mlx90640

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
    def init_mlx90640():
        i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)
        mlx = adafruit_mlx90640.MLX90640(i2c)
        mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ
        logging.debug("MLX addr detected on I2C", [hex(i) for i in mlx.serial_number])
        return mlx
    
    @staticmethod
    def process_frame(frame, temp_range):
        thermal_matrix = np.array(frame).reshape(24, 32)
        blurred_matrix = cv2.GaussianBlur(thermal_matrix, (5, 5), 0)
        _, thresholded_matrix = cv2.threshold(blurred_matrix, temp_range[0], temp_range[1], cv2.THRESH_BINARY)
        thresholded_matrix = thresholded_matrix.astype(np.uint8) * 255
        contours, _ = cv2.findContours(thresholded_matrix, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            return np.zeros_like(thresholded_matrix), 0
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        largest_region = np.zeros_like(thresholded_matrix)
        cv2.drawContours(largest_region, [contours[0]], 0, 255, thickness=cv2.FILLED)
        return largest_region, thermal_matrix.max()

    @staticmethod
    def print_results(thresholded_matrix, highest_temp):
        for row in thresholded_matrix:
            print(", ".join(["%d" % (value//255) for value in row]))
        print("_______")

    @staticmethod
    def find_centroid_difference(thresholded_matrix):
        
        y_positions, x_positions = np.where(thresholded_matrix == 255)
        if len(x_positions) == 0 or len(y_positions) == 0:
            return None, (0, 0)
        centroid_x = int(np.mean(x_positions))
        centroid_y = int(np.mean(y_positions))
        difference_x = centroid_x - IMAGE_CENTER_POINT_X
        difference_y = centroid_y - IMAGE_CENTER_POINT_Y
        return (centroid_x, centroid_y), (difference_x, difference_y)

    @staticmethod
    def thermal_detection(callback, temp_range):
        mlx = VideoUtils.init_mlx90640()
        frame = [0] * 768
        frame_interval = 1.0 / 16
        program_time = time.time()
        frame_count = 0
        restart_count = 0
        try:
            while True:
                try:
                    logging.debug("start new frame")
                    start_time = time.time()
                    mlx.getFrame(frame)
                    image_time = time.time()

                    thresholded_matrix, highest_temp = VideoUtils.process_frame(frame, temp_range)
                    centroid, difference_to_center = VideoUtils.find_centroid_difference(thresholded_matrix)


                    if centroid:
                        logging.debug(f'Difference from the most central point: {difference_to_center}')
                        callback(centroid, difference_to_center)

                    elapsed_time = time.time() - start_time
                    logging.debug("--- total %s seconds ---" % (time.time() - start_time))
                    logging.debug("--- read image time %s seconds ---" % (image_time - start_time))
                    logging.debug("--- image process %s seconds ---" % (time.time() - image_time))
                    frame_count += 1

                    if elapsed_time < frame_interval:
                        logging.info("Sleeping for : %s" % (frame_interval - elapsed_time))
                        time.sleep(frame_interval - elapsed_time)
                except:
                    logging.warning('Error reading frame')
                    restart_count += 1
                    continue
        except RuntimeError:
            logging.warning("tooooooooooooooooo  many  retries")
            logging.info("detection time : %s" % (time.time() - program_time))
            logging.info('Total frames count: '+str(frame_count))
            logging.info("Restart Count : %s" % restart_count)
            exit(1)
        except KeyboardInterrupt:
            logging.debug("Key Board Interrupt")
            logging.info("detection time : %s" % (time.time() - program_time))
            logging.info('Total frames count: '+str(frame_count))
            logging.info("Restart Count : %s" % restart_count)
            exit(0)