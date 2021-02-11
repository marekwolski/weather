import sys, time, logging, scrollphathd
import requests, json

def scroll_message(message):
    scrollphathd.clear()                         # Clear the display and reset scrolling to (0, 0)
    scrollphathd.rotate(degrees=180)
    length = scrollphathd.write_string(message, x=17, brightness=0.1)  # Write out your message
    scrollphathd.show()                          # Show the result
    time.sleep(0.2)                              # Initial delay before scrolling

    length += scrollphathd.width
    # Now for the scrolling loop...
    while length > 0:
        scrollphathd.scroll(1)                   # Scroll the buffer one place to the left
        scrollphathd.show()                      # Show the result
        length -= 1
        time.sleep(0.02)                         # Delay for each scrolling step

    time.sleep(0.2)                              # Delay at the end of scrolling


def get_temp():
    url = 'http://192.168.1.17:8080/json'

    scrollphathd.clear()                         # Clear the display and reset scrolling to (0, 0)
    scrollphathd.rotate(degrees=180)
    scrollphathd.write_string('GET', brightness=0.1)  # Write out your message
    scrollphathd.show()                          # Show the result

    try:
        logging.info('Get updated stats ...')
        r = requests.get(url)
    except:
        logging.warning('Tried to get the json stats but now in the exception code')
        the_stats = "Error getting temp! Error getting pressure!"
    else:
        stats = json.loads(r.content)
        logging.info(stats)
        the_stats = f"{stats['temp']:.1f}" + 'c  ' + f"{stats['pressure']:.0f}" + 'hPa'

    scrollphathd.clear()                         # Clear the display and reset scrolling to (0, 0)
    scrollphathd.show()                          # Show the result
    return the_stats

#
# Let's get started ...
#
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    filename='scrolltemp.log')
logging.info('SCROLLING STARTED ...')

while True:
    scrolltext = get_temp()
    logging.info('Scroll this: %s', scrolltext)
    for i in range(10):
        scroll_message(scrolltext)
