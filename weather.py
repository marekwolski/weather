from flask import Flask, render_template, request

from datetime import datetime
import time
from bme280 import BME280


# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = f.read()
        temp = int(temp) / 1000.0
    return temp



app = Flask(__name__)

@app.route("/")
def hello():
   try:
       from smbus2 import SMBus
   except ImportError:
       from smbus import SMBus

   bus = SMBus(1)
   bme280 = BME280(i2c_dev=bus)
   # throw away reading, first one is inaccurate
   x = bme280.get_temperature()
   time.sleep(1)
   
   ts = [bme280.get_temperature()] * 10
   ps = [bme280.get_pressure()] * 10
   hs = [bme280.get_humidity()] * 10

   #print(ts)
   #print(ps)
   #print(hs)

   wts = (sum(ts) / len(ts))
   wps = (sum(ps) / len(ps))
   whs = (sum(hs) / len(hs))


   # Tuning factor for compensation. Decrease this number to adjust the
   # temperature down, and increase to adjust up
   factor = 2.25
   cpu_temps = [get_cpu_temperature()] * 5
   cpu_temp = get_cpu_temperature()
   # Smooth out with some averaging to decrease jitter
   cpu_temps = cpu_temps[1:] + [cpu_temp]
   avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
   raw_temp = wts
   comp_temp = raw_temp - ((avg_cpu_temp - raw_temp) / factor)
   #logging.info("Compensated temperature: {:05.2f} *C".format(comp_temp))

   templateData = {
      'title' : 'Weather Report',
      'temp': f"{comp_temp:05.2f}",
      'pressure': f"{wps:07.2f}",
      'humidity': f"{whs:05.2f}",
      'time': datetime.now().strftime("%Y-%m-%d %H:%M")
      }
   return render_template('main.html', **templateData)


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True)
