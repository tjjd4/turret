import cv2
import time
import board
import busio
import numpy as np
import adafruit_mlx90640

def init_mlx_sensor():
    i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)
    mlx = adafruit_mlx90640.MLX90640(i2c)
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ
    print("MLX addr detected on I2C", [hex(i) for i in mlx.serial_number])
    return mlx

def process_frame(frame):
    thermal_matrix = np.array(frame).reshape(24, 32)
    blurred_matrix = cv2.GaussianBlur(thermal_matrix, (5, 5), 0)
    _, thresholded_matrix = cv2.threshold(blurred_matrix, TEMP_RANGE[0], TEMP_RANGE[1], cv2.THRESH_BINARY)
    thresholded_matrix = thresholded_matrix.astype(np.uint8) * 255
    contours, _ = cv2.findContours(thresholded_matrix, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return np.zeros_like(thresholded_matrix), 0
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    largest_region = np.zeros_like(thresholded_matrix)
    cv2.drawContours(largest_region, [contours[0]], 0, 255, thickness=cv2.FILLED)
    return largest_region, thermal_matrix.max()

def print_results(thresholded_matrix, highest_temp):
    for row in thresholded_matrix:
        print(", ".join(["%d" % (value//255) for value in row]))
    print("_______")

def find_centroid_difference(thresholded_matrix):
    central_point = (15, 11)
    y_positions, x_positions = np.where(thresholded_matrix == 255)
    if len(x_positions) == 0 or len(y_positions) == 0:
        return None, (0, 0)
    centroid_x = int(np.mean(x_positions))
    centroid_y = int(np.mean(y_positions))
    difference_x = centroid_x - central_point[0]
    difference_y = centroid_y - central_point[1]
    return (centroid_x, centroid_y), (difference_x, difference_y)

def print_temperature(frame):
    thermal_matrix = np.array(frame).reshape(24,32)
    for row in thermal_matrix:
        print(', '.join(map(lambda x: str(int(x)), row)))
    print('________')

def print_highest_temperature_matrix(frame):
    thermal_matrix = np.array(frame).reshape(24, 32)
    max_temp = thermal_matrix.max()
    y, x = np.where(thermal_matrix == max_temp)
    
    # Reset all values to zero
    thermal_matrix[:] = 0
    
    if len(x) > 0 and len(y) > 0:
        thermal_matrix[y[0], x[0]] = max_temp
        
    for row in thermal_matrix:
        print(', '.join(map(lambda x: str(int(x)), row)))
    print('________')

def thermal_detection_modified():
    mlx = init_mlx_sensor()
    frame = [0] * 768
    frame_interval = 1.0 / 16

    # Prompt user input only once at the start
    user_input = input("Press 't' to display temperature, 'q' to find centroid difference, or 'h' to show the highest temperature point: ")
    show_temperature = True if user_input == 't' else False
    show_highest_temp = True if user_input == 'h' else False

    try:
        while True:
            start_time = time.time()
            print("start next frame")
            mlx.getFrame(frame)
            print("frame get")

            # If user chose to show temperature
            if show_temperature:
                print_temperature(frame)
            elif show_highest_temp:
                print_highest_temperature_matrix(frame)
            else:
                thresholded_matrix, _ = process_frame(frame)
                centroid, difference_to_center = find_centroid_difference(thresholded_matrix)
                if centroid:
                    print(f'Centroid of temperature in range: {centroid}')
                    print(f'Difference from the most central point: {difference_to_center}')
                else:
                    print('No Centroid found')
                print_results(thresholded_matrix, _)

            elapsed_time = time.time() - start_time
            print("--- total %s seconds ---" % (time.time() - start_time))

            if elapsed_time < frame_interval:
                print("Sleeping for : %s" % (frame_interval - elapsed_time))
                time.sleep(frame_interval - elapsed_time)
                
    except ValueError:
        print('Error reading frame')
    except RuntimeError:
        print("Too many retries")
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        raise KeyboardInterrupt

if __name__ == "__main__":
    TEMP_RANGE = (30, 40)
    count = 0
    while True:
        try:
            thermal_detection_modified()
        except Exception as e:
            pass
        except KeyboardInterrupt:
            print("Program end")
            print("Restart Count : %s" % count)
            break
        count += 1