im at camp, might be a few days until more updates 
# Mouselink

[Mouselink on PyPI](https://pypi.org/project/mouselink/)

better documentation/readme coming soon

Mouselink is a Python package that emulates [Scratch Link](https://scratch.mit.edu/download/scratch-link), which enables Scratch to connect to hardware peripherals such as a micro:bit or an EV3. Mouselink tricks Scratch into thinking that it *is* Scratch Link, and allows you to connect Scratch to more then their small selection of hardware peripherals, and to software as well!

## Installation

To install it, use:

```bash
python -m pip install mouselink
```

You can use the example code found in the `examples` directory or copy the code below:

```python
from mouselink import mouselink as sl

p = sl.ev3()

def on_got_data(data):
    print(f"Got data: {data}")
    p.send(f"1{data}0") # send back data with some additional data

p.on_read(on_got_data)

p.run()
```

## Developing Mouselink

Clone the repo

```bash
git clone https://github.com/minniesBaa/mouselink.git
```

To test changes, run `build-and-test.bat` to build and install.

## Features (and planned ones)

### Implemented

- Add an EV3 to the device list
- Allow Scratch to connect to that EV3
- Transmit data as that EV3

### Planned

- Support connecting as other peripherals
  - micro:bit
  - WeDo 2.0
- Allow for more peripherals (like LEGO Spike/RI)
- Custom firmware for peripherals
- Communication using the Translate extention's data saving glitch
