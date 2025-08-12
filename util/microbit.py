from mouselink import mouselink
microbit = mouselink.microbit()
def on_read(e):
    print(f"Data recieved: {e}")
    #microbit.send("1100101010101010110101010100")
    microbit.send("100110110011001")
    microbit.send("10100111111101111111")
microbit.on_read(on_read)
microbit.run()
