import time
import board
import busio
import numpy as np
import adafruit_mlx90640

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C", [hex(i) for i in mlx.serial_number])

# if using higher refresh rates yields a 'too many retries' exception,
# try decreasing this value to work with certain pi/camera combinations
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

frame = np.zeros((24*32,))

while True:
    try:
        mlx.getFrame(frame)
    except ValueError:
        # these happen, no biggie - retry
        continue
    
    w, h = frame.shape[:2]
    print(w,h)

    # thermal_matrix =np.array(frame).reshape(24, 32)
    # highest_temp = thermal_matrix.max()
    # thermal_matrix[thermal_matrix != highest_temp] = 0
    # thermal_img = thermal_matrix.tolist()
    for h in range(24):
        for w in range(32):
            t = frame[h*32 + w]
            print("%0.1f, " % t, end="")
        print()
    print()
