from flask import Flask, render_template, jsonify
from datetime import datetime
import time
from bme280 import BME280

# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = f.read()
        temp = int(temp) / 1000.0
    return temp

def get_data():
   try:
       from smbus2 import SMBus
   except ImportError:
       from smbus import SMBus

   bus = SMBus(1)
   bme280 = BME280(i2c_dev=bus)
   # throw away reading, first one is inaccurate
   unused = bme280.get_temperature()
   time.sleep(1)
   
   ts = [bme280.get_temperature()] * 10
   ps = [bme280.get_pressure()] * 10
   hs = [bme280.get_humidity()] * 10

   wts = (sum(ts) / len(ts))
   wps = (sum(ps) / len(ps))
   whs = (sum(hs) / len(hs))

   # Tuning factor for compensation. Decrease this number to adjust the
   # temperature down, and increase to adjust up
   factor = 1.5
   cpu_temps = [get_cpu_temperature()] * 5
   cpu_temp = get_cpu_temperature()
   # Smooth out with some averaging to decrease jitter
   cpu_temps = cpu_temps[1:] + [cpu_temp]
   avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
   raw_temp = wts
   comp_temp = raw_temp - ((avg_cpu_temp - raw_temp) / factor)

   sensordata = {
      'sensor_temp': comp_temp,
      'sensor_pressure': wps,
      'sensor_humidity': whs
      }
   return sensordata


app = Flask(__name__)

@app.route("/ping")
def ping():
   return "Ping! (" + datetime.now().strftime("%Y-%m-%d %H:%M") + ")"

@app.route("/")
def hello():
   data = get_data() 
   now = datetime.now()
   templateData = {
      'title' : 'Weather Report',
      'temp': f"{data['sensor_temp']:+.1f}",
      'pressure': f"{data['sensor_pressure']:.1f}",
      'humidity': f"{data['sensor_humidity']:.1f}",
      'time': f"{now:%Y-%m-%d %H:%M}"
      }
   return render_template('main.html', **templateData)

@app.route("/json")
def sendjson():
   data = get_data()
   now = datetime.now()
   templateData = {
      'temp': data['sensor_temp'],
      'pressure': data['sensor_pressure'],
      'humidity': data['sensor_humidity'],
      'time_id': now.timestamp(),
      'time': now
      }
   return jsonify(templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True)
