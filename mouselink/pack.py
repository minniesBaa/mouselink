"""
File for packaging values into base64'd packets readable by Scratch
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