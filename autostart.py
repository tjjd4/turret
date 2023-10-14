if __name__ == '__main__':
    import sys
    import time
    import logging
    import threading
    import signal
    from src.turret import Turret

    logging.getLogger().setLevel(logging.WARNING)

    def start_turret(signum, frame):
        turret_thread = threading.Thread(target=t.start)
        turret_thread.daemon = True
        turret_thread.start()

    def stop_turret(signum, frame):
        t.stop()

    # Initialize the turret
    t = Turret()

    # Register signal handlers
    signal.signal(signal.SIGUSR1, start_turret)
    signal.signal(signal.SIGUSR2, stop_turret)

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            # Handle Ctrl+C to gracefully exit the program
            t.stop()
            sys.exit()