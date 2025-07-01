import mouselink as sl

p = sl.ev3()

def on_read(data):
    print(f"Got data: {data}")
    p.send(f"111{data}")

p.on_read(on_read)

p.run()