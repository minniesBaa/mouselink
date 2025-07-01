import mouselink as sl # import mouselink

p = sl.ev3() # set "p" to an ev3 object

def on_got_data(data): # function to handle recieved data
    print(f"Got data: {data}") # post the data recieved to the console
    p.send(data) # echo the data back

p.on_read(on_got_data) # tell mouselink to call "on_got_data" whenever it gets data from Scratch

p.run() # start mouselink