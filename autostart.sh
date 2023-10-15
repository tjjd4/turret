#!/bin/bash

# Run `pigs t` and capture its output
output=$(pigs t)

# Check if the output contains a number using a regular expression
if [[ "$output" =~ [0-9]+ ]]; then
    echo "pigpiod activated: $output"
else
    echo "pigpiod is not activated..."
    sudo pigpiod
fi

python3 /home/billy/Desktop/turret/autostart.py