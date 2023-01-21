import board
import digitalio
import adafruit_max31865

def setupSensor(clockPin):
    spi = board.SPI()
    cs = digitalio.DigitalInOut(clockPin)  # Chip select of the MAX31865 board.
    sensor = adafruit_max31865.MAX31865(spi, cs, wires=3, rtd_nominal=100.0, ref_resistor=430.0)
    return sensor

def readTemp(sensor):
    rtn = {'tempC': sensor.temperature,
            'tempF': convertCtoF(sensor.temperature),
            'resistance': sensor.resistance,
            'auto-conver': sensor.auto_convert,
            'bias': sensor.bias,
            'fault': sensor.fault}

    return rtn
    
def convertCtoF(cel):
    return (cel * 1.8) + 32

if __name__ == "__main__":
    sensor = setupSensor(board.D5)
    rtn = readTemp(sensor)
    print(rtn)