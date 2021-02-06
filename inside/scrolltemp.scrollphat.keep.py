import sys, time, logging, scrollphat
import requests, json

def scroll_once():
    length = scrollphat.buffer_len()
    for x in range(length):    
        scrollphat.scroll()
        time.sleep(0.1)

def get_temp():
    url = 'http://192.168.1.17:8080/json'
    try:
        logging.info('Get updated stats ...')
        r = requests.get(url)
    except:
        logging.warning('Tried to get the json stats and now in the exception code')
        the_temp = "Error getting temp!"
        the_pressure = "Error getting pressure!"
    else:
        stats = json.loads(r.content)
        logging.info(stats)
        the_temp = f"{stats['temp']:.1f}"
        the_pressure = f"{stats['pressure']:.0f}"

    the_stats = the_temp + 'C  ' + the_pressure + 'hPa'
    return the_stats

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    filename='scrolltemp.log')

scrollphat.set_brightness(2)
scrollphat.set_rotate(True)
logging.info('SCROLLING STARTED ...')

while True:
    scrollphat.clear()
    scrolltext = get_temp()
    scrollphat.write_string(scrolltext, 11)
    logging.info('Scroll this: %s', scrolltext)
    for i in range(6):
        scroll_once()
