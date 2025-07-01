import struct
import base64
def _pack_float(float):
    b = list(struct.pack("f", float))
    return b
def _add_filler_vals_dist(data):
    prefix = [35,0,0,0,2]
    suffix = [126,126,126,126,126,126,126,126,126,126,126,126,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 
    return prefix + data + suffix
def _b64ify(data):
    return base64.b64encode(bytes(data)).decode('ascii')
def pack_dist(num):
    return _b64ify(_add_filler_vals_dist(_pack_float(num)))