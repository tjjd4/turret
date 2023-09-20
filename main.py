from turret import Turret

if __name__ == '__main__':

    user_input = input("Choose an mode: (1) Thermal Tracking (2) Customize Setting \n")
    if str(user_input) == "1":
        t = Turret()
        t.calibrate()
        t.thermal_tracking()
    elif str(user_input) == "2":
        low_temp = input("Setting: detect temp range from ? (Type the lowest temperture be detected)\n")
        try:
            low = int(low_temp)
        except:
            print("Invalid input. Please enter a valid integer.")
            exit(1)
        high_temp = input(f"Setting: detect temp range from {low} to ? (Type the highest temperture be detected)\n")
        try:
            high = int(high_temp)
        except:
            print("Invalid input. Please enter a valid integer.")
            exit(1)
        if low >= high:
            print("Invalid input. From 'low' to 'high'.")
            exit(1)
        else:
            t = Turret((low, high))
            t.calibrate()
            t.thermal_tracking()

    else:
        print("Unknown input mode. Please choose a number (1) or (2)")

