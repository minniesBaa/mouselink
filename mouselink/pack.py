"""
File for packaging/unpackaging values/base64
"""

import struct
import base64
import math
def _pack_float(float):
    # package a 32-bit float into a list of numbers
    b = list(struct.pack("f", float))
    return b
def _add_filler_vals_dist(data):
    # add filler values for the EV3 distance reporter
    prefix = [35,0,0,0,2]
    suffix = [126,126,126,126,126,126,126,126,126,126,126,126,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 
    return prefix + data + suffix
def _b64ify(data):
    # convert a list of numbers to base64
    return base64.b64encode(bytes(data)).decode('ascii')
def _unpk(data):
    # convert base64 to list
    return list(base64.b64decode(str(data).encode('ascii')))
def pack_dist(num):
    # makes a base64 with a specific value in the 'distance' reporter
    return _b64ify(_add_filler_vals_dist(_pack_float(num)))
def _convert_note_bytes(num1, num2):
    # convert note bytes to notes
    return round(12*math.log2((num2*256+num1)/440)+57)
def bytes_to_decimal(num1, num2):
    # convert two bytes from Scratch to an int
    return num2*256+num1
def reconstruct_matrix(data):
    p0 = data[1]
    p1 = data[2]<<5
    p2 = data[3]<<10
    p3 = data[4]<<15
    p4 = data[5]<<20
    return bin(p0|p1|p2|p3|p4)[2:].zfill(25)[::-1]
def microbit_load_matrix(data):
    return reconstruct_matrix(_unpk(data))
def microbit_build_sensors(sensors):
    tiltX = [sensors[0] * 10 >> 8, sensors[0] * 10 & 0xff]
    tiltY = [sensors[1] * 10 >> 8, sensors[1] * 10 & 0xff]
    buttonA = 1 if sensors[2] else 0
    buttonB = 1 if sensors[3] else 0
    touchpin1 = 1 if sensors[4][0] else 0
    touchpin2 = 1 if sensors[4][1] else 0
    touchpin3 = 1 if sensors[4][2] else 0
    gesture = int(f"{1 if sensors[5] else 0}{1 if sensors[5] else 0}{1 if sensors[5] else 0}")
    data = []
    data.extend(tiltX)
    data.extend(tiltY)
    data.append(buttonA)
    data.append(buttonB)
    data.append(touchpin1)
    data.append(touchpin2)
    data.append(touchpin3)
    data.append(gesture)
    print(data)
    return _b64ify(data)
def _split_bits_microbit(data,bit):
    data = str(data).zfill(27)
    breakoutindexes = [10,10,1,1,1,1,"bit",3]
    buffer = ""
    res = []
    for i in range(25):
        buffer += data[i]
        if len(buffer) == breakoutindexes[0]:
            del(breakoutindexes[0])
            res.append(buffer)
            buffer = ""
        elif breakoutindexes[0] == "bit":
            del(breakoutindexes[0])
            res.append(bit)
            buffer = ""
    return res
def _make_microbit_msg(data, bit):
    return microbit_build_sensors(_split_bits_microbit(data, bit))