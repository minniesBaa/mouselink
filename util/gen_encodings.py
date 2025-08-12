formats = {
    "english": {
        "prefix": "01",  # 2 digit prefix pattern for format identification
        "bits": 6,       # amount of bits used by each character, must be a factor of 18 (20 total bits - 2 prefix bits)
        "charset":       # set of characters to be used in encoding, must be 2^bits in length
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .,?!\"'()$-_"
    },
}

def build_formats():
    builtformats = {}
    for fname in formats.keys():
        format = formats[fname]
        counter = 0
        built = {}
        for char in format["charset"]:
            built[char] = str(bin(counter))[2:].zfill(format["bits"])
            counter +=1
        builtformat = [format["prefix"], 18 / format["bits"], built]
        builtformats[fname] = builtformat
    print(builtformats)
build_formats()