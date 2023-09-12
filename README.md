# Turret

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

### Using pipenv
> To install `pipenv`
> ```bash
> pip install --user pipenv
> ```
Using Python virtualenv management tool [pipenv](https://pipenv.pypa.io/en/latest/) to install and isolate python package.

Install the dependencies from `pipfile`

```bash
pipenv install
```

If the requirements.txt not found or outdated, you may recreate it with `pipfile` from pipenv:
```bash
pip install
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
