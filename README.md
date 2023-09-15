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
  ### Adafruit_CircuitPython_MLX90640
  Original Repository : [Adafruit_CircuitPython_MLX90640](https://github.com/adafruit/Adafruit_CircuitPython_MLX90640.git)
  The original repository (python) is unable to use the frequency above 8 Hz with thermal camera.
  To make is work on 8 Hz and above, it is needed to make some changes in the original repository.
  Edited Repository ( 8 Hz and above frequency enable ) : [Adafruit_CircuitPython_MLX90640](https://github.com/seantjjd4/Adafruit_CircuitPython_MLX90640.git)

  ```bash
  git clone https://github.com/seantjjd4/Adafruit_CircuitPython_MLX90640.git
  # in your project enviroment
  pip install -e /path/to/Adafruit_CircuitPython_MLX90640/
  
  ```

## Usage

```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
