"""
File for packaging values into base64'd packets readable by Scratch
"""

import struct
import base64
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
def pack_dist(num):
    return _b64ify(_add_filler_vals_dist(_pack_float(num)))