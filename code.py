import board
import digitalio
import analogio
import time
import supervisor

PIN_NO2 = analogio.AnalogIn(board.A0)
resistor = 10  # pull up resistor in KOhms

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

while True:
    current_time = time.time()
    voltage = (PIN_NO2.value / 65535) * PIN_NO2.reference_voltage
    resistance = (PIN_NO2.value / 65535) * resistor

    print("Time: " + str(current_time))
    print("Voltage: " + str(voltage) + "v")
    print("Resistance: " + str(resistance) + "KOhms")

    led.value = supervisor.runtime.usb_connected
    if not supervisor.runtime.usb_connected:
        print("Writing to file")
        with open("/results.csv", "a") as file:
            led.value = True
            file.write("{0},{1:f},{2:f}\n".format(current_time, voltage, resistance))
            file.flush()
            led.value = False
            time.sleep(10)
    else:
        time.sleep(1.0)

