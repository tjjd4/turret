if __name__ == '__main__':
    import logging
    from src.turret import Turret

    user_input = input("Choose an mode: (1) Thermal Tracking (2) Customize Setting \n")
    if str(user_input) == "1":
        logging.getLogger().setLevel(logging.DEBUG)
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
        

        log_level = input("Logger level: (1) debug (2) info\n")

        try:
            level = int(log_level)
            if level == 1:
                logging.getLogger().setLevel(logging.DEBUG)
            elif level == 2:
                logging.getLogger().setLevel(logging.INFO)

        except:
            print("Invalid input. Please enter the valid integer 1 or 2.")
            exit(1)
        
        t = Turret((low, high))
        t.calibrate()
        t.thermal_tracking()

    else:
        print("Unknown input mode. Please choose a number (1) or (2)")

