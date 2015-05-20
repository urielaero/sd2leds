#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
import signal
import sys

import logging
import logging.handlers

#logs:
# Deafults
LOG_FILENAME = "/tmp/myservicetest.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"
# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
# Give the logger a unique name (good practice)
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)


GPIO.setmode(GPIO.BOARD)
leds = [18,16,12,10,8,11]
for i in leds:
    GPIO.setup(i, GPIO.OUT)

for i in leds:
    GPIO.output(i,False)
    GPIO.output(i,True)

def secuence():
    for i in leds:
        GPIO.output(i,False)
        time.sleep(1)
        GPIO.output(i,True)


 
def signal_term_handler(signal, frame):
    logger.info('got SIGTERM')
    GPIO.cleanup()
    sys.exit(0)
 
signal.signal(signal.SIGTERM, signal_term_handler)    

if __name__=="__main__":
    logger.info( "test" )
    try:
        while 1:
            secuence()
            time.sleep(.05)
    except KeyboardInterrupt,e:
        GPIO.cleanup()
        #print "clear"

