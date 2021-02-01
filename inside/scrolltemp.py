import sys, time, scrollphat
import requests, json

def scroll_once():
    length = scrollphat.buffer_len()
    for x in range(length):    
        scrollphat.scroll()
        time.sleep(0.1)

def get_temp():
    url = 'http://192.168.1.17:8080/json'
    try:
        r = requests.get(url)
        stats = json.loads(r.content)
        #print(stats)
        the_temp = f"{stats['temp']:.1f}"
        the_pressure = f"{stats['pressure']:.0f}"
    except:
        the_temp = "Error getting temp!"
        the_pressure = "Error getting pressure!"
    print('Temperature is ', the_temp, ' & the Pressure is ', the_pressure)
    the_stats = the_temp + 'C  ' + the_pressure + 'hPa'
    return the_stats


scrollphat.set_brightness(2)
scrollphat.set_rotate(True)

while True:
    scrollphat.clear()
    scrollphat.write_string(get_temp(), 11)
    for i in range(6):
        scroll_once()
