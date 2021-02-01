import time
from bme280 import BME280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

import logging

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("""weather.py - Print readings from the BME280 weather sensor.

Press Ctrl+C to exit!

""")

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

x = bme280.get_temperature()
print(x)
time.sleep(1)

ts = [bme280.get_temperature()] * 4
ps = [bme280.get_pressure()] * 4
hs = [bme280.get_humidity()] * 4

print(ts)
print(ps)
print(hs)

print(sum(ts) / len(ts))
print(sum(ps) / len(ps))
print(sum(hs) / len(hs))



while True:
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()
    logging.info("""Temperature: {:05.2f} *C
Pressure: {:05.2f} hPa
Relative humidity: {:05.2f} %
""".format(temperature, pressure, humidity))
    time.sleep(1)
