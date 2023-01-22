import board
import digitalio
import adafruit_max31865

spi = board.SPI()
cs = digitalio.DigitalInOut(board.D5)  # Chip select of the MAX31865 board.
sensor = adafruit_max31865.MAX31865(spi, cs, wires=3, rtd_nominal=100.0, ref_resistor=430.0)

print('Temperature: {0:0.3f}C'.format(sensor.temperature))
print('Resistance: {0:0.3f} Ohms'.format(sensor.resistance))

print('auto-conver: {}'.format(sensor.auto_convert))
print('bias: {}'.format(sensor.bias))
print('fault: {}'.format(sensor.fault))

if __name__ == "__main__":
    main()