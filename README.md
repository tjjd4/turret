Turret
=============================

This is a python program control automatic turret with termal camera through Raspberry Pi

## Matirial
single-board computers : [Raspberry Pi 4 model b](https://piepie.com.tw/product/raspberry-pi-4-model-b-4gb)

Motors : [K-Power Hb200t * 2](https://www.made-in-china.com/showroom/servo-kyra/product-detailTyEQoAuWXwhO/China-K-Power-Hb200t-12V-200kg-Torque-Steel-Gear-Digital-Industrial-Servo.html)

Thermal Camera: [MLX90640-BAA IR Thermal Camera](https://twarm.com/commerce/product_info.php?products_id=7218)

## Raspberry Pi Setup
[How to set up a Raspberry Pi](https://www.raspberrypi.com/tutorials/how-to-set-up-raspberry-pi/)


## Installation

  ### Using `pip`
  Use the package manager [pip](https://pip.pypa.io/en/stable/) to install python package.
  Install the dependencies from `requirements.txt`
  
  ```bash
  pip install
  ```
  
  If the `requirements.txt` not found or outdated, you may have to use `pipenv`

  ### Using `pipenv`
  Using Python virtualenv management tool [pipenv](https://pipenv.pypa.io/en/latest/) to install and isolate python packages from other projects.
  
  > To install `pipenv`
  > ```bash
  > pip install --user pipenv
  > ```
  
  Install the dependencies from `pipfile`
  
  ```bash
  pipenv install
  ```
  Install the dependencies from `requirements.txt`
  ```bash
  pipenv install -r path/to/requirements.txt
  ```
  
  If the `requirements.txt` not found or outdated, you may recreate it with `pipfile` from  `pipenv`:
  ```bash
  pipenv lock -r > requirements.txt
  ```
  ### Error installing opencv-python
  Sometime opencv-python couldn't be installed on Raspberry Pi. The installation will stuck in likely the last step, pending something forever.
  In this case, you may install the older version of opencv-python.
  e.g.:
  ```bash
  pip install opencv-python==4.4.0.46
  ```
  ### Adafruit_CircuitPython_MLX90640
  **Original Repository** : [Adafruit_CircuitPython_MLX90640](https://github.com/adafruit/Adafruit_CircuitPython_MLX90640.git)
  
  The original repository (python) is unable to use the frequency above 8 Hz with thermal camera.
  
  To make is work on 8 Hz and above, it is needed to make some changes in the original repository.
  
  **Edited Repository ( 8 Hz and above frequency enable )** : [Adafruit_CircuitPython_MLX90640](https://github.com/seantjjd4/Adafruit_CircuitPython_MLX90640.git)

  ```bash
  git clone https://github.com/seantjjd4/Adafruit_CircuitPython_MLX90640.git

  # in your project enviroment
  pip install -e /path/to/Adafruit_CircuitPython_MLX90640/
  
  ```

## Usage

```bash
cd /path/to/project_folder

python3 main.py
```
### To Run Test
```bash
python3 -m unittest

# to run specific test file
python3 -m unittest test/test_file
```
## Set Auto Start
There are serveral autostart methods in raspberry pi.

### Systemd service setting
Using systemd service unit for auto start raspberry pi project
1. Create a systemd service unit file
```bash
sudo nano /etc/systemd/system/turret-autostart.service
```
2. Add the following content to the turret-autostart.service file
```bash
[Unit]

Description=Turret program autostart service

[Service]

ExecStart=/bin/bash /path/to/turret/autostart.sh

Restart=on-failure

User=${user-name}

[Install]

WantedBy=multi-user.target
```
3. Reload systemd to read the new service unit after save the file
```bash
sudo systemctl daemon-reload
```
4. Enable the service to your project
```bash
sudo systemctl enable turret-autostart.service
```
5. Start your service
```bash
sudo systemctl start turret-autostart.service
```
### Restart and check the status!
Restart:
```bash
sudo reboot
```
Check service status and log:
```bash
sudo systemctl status turret-autostart.service
```
Check python program:
```bash
ps aux | grep python
```
## System Workflow
![使用流程圖 drawio](https://github.com/tjjd4/turret/assets/61817112/7068c9a0-1762-46b2-a909-eb501806e91f)

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
