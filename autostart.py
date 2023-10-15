'''
This version is set up for turret project could be
control over two button -- on, off -- to activate and turn off.
The GPIO Pin should be specific
'''
GPIO_ON = 17
GPIO_OFF = 27

if __name__ == '__main__':
    import sys
    import time
    import logging
    import pigpio
    from src.pi import Pi
    from src.turret import Turret

    logging.getLogger().setLevel(logging.WARNING)

    pi4 = Pi()
    # Initialize the turret
    t = Turret(pi4=pi4)
    t.calibrate()
    pi4.callback(GPIO_ON, pigpio.FALLING_EDGE, t.start)
    pi4.callback(GPIO_OFF, pigpio.FALLING_EDGE, t.stop)
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            # Handle Ctrl+C to gracefully exit the program
            t.off()
            sys.exit()