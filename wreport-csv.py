import time, os
from datetime import datetime
from bme280 import BME280

# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = f.read()
        temp = int(temp) / 1000.0
    return temp

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

x = bme280.get_temperature()
#print(x)
time.sleep(1)

ts = [bme280.get_temperature()] * 5
ps = [bme280.get_pressure()] * 5
hs = [bme280.get_humidity()] * 5

#print(ts)
#print(ps)
#print(hs)

# Tuning factor for compensation. Decrease this number to adjust the
# temperature down, and increase to adjust up
factor = 2.25
cpu_temps = [get_cpu_temperature()] * 5
cpu_temp = get_cpu_temperature()
# Smooth out with some averaging to decrease jitter
cpu_temps = cpu_temps[1:] + [cpu_temp]
avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
raw_temp = (sum(ts) / len(ts))
comp_temp = raw_temp - ((avg_cpu_temp - raw_temp) / factor)

wts = f"{comp_temp:05.2f}"
wps = f"{(sum(ps) / len(ps)):07.2f}"
whs = f"{(sum(hs) / len(hs)):05.2f}"
tstamp = datetime.now().strftime("%Y-%m-%d %H:%M")

statsfilepath = os.path.expanduser('~/')
statsfilename = statsfilepath + 'wstats_' + datetime.today().strftime('%Y-%m-%d') + '.csv'

with open(statsfilename, "a") as statsfile:
    row = tstamp + ', ' + wts + ', ' + wps + ', ' + whs
    #print(row)
    statsfile.write(row + "\n")
