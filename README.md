# Mouselink
[Mouselink on PyPI](https://pypi.org/project/mouselink/)

Mouselink is a Python package that emulates [Scratch Link](https://scratch.mit.edu/download/scratch-link), which enables Scratch to connect to hardware peripherals such as a micro:bit or an EV3. Mouselink tricks Scratch into thinking that it *is* Scratch Link, and allows you to connect Scratch to more then their small selection of hardware peripherals, and to software as well!
## Installation
To install it, use:
```
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
## Features (and planned ones)
### Implemented:
 - Add an EV3 to the device list
 - Allow Scratch to connect to that EV3
 - Transmit data as that EV3
### Planned
 - Support connecting as other peripherals
   - micro:bit
   - WeDo 2.0
 - Communication using the Translate extention's data saving glitch
## How does it work?
I investigated Scratch's communication with Scratch Link, and discovered it uses a plain, unencrypted WebSocket server. I own an EV3, so I used my web browser's developer tools to monitor the data sent between Scratch and Scratch Link. I then began writing Mouselink, using my real EV3 communication as reference for the protocol. After a few days, I could connect an emulated EV3 device and have it be recognised by Scratch, and a few days after that I could transmit data between Scratch and Mouselink.