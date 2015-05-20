#!/usr/bin/env python
from time import sleep
import RPi.GPIO as GPIO
import threading
import subprocess
import signal
import sys
import logging
import logging.handlers

GPIO.setmode(GPIO.BOARD)

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

def signal_term_handler(signal, frame):
    logger.info('got SIGTERM')
    GPIO.cleanup()
    sys.exit(0)
 
signal.signal(signal.SIGTERM, signal_term_handler)    



class Secuence(object):

    def __init__(self,pause=1):

        self.sec = [
            [#secuencia 1
                [False,True,False,True,False,True],
                [True,False,True,False,True,False]
            ],
            [
                [True,False,False,False,False,True],
                [False,True,False,False,True,False],
                [False,False,True,False,False,True],
                [False,False,False,True,True,True]
            ],
            [
                [False,True,True,False,False,False],
                [True,False,False,True,True,True]
            ]
        ]
        self.sec = []

        self.restoreState = False

        self.leds = [18,16,12,10,8,11]
        self.pause = pause

        self.button1 = 13
        self.button2 = 15
        self.button3 = 7

        self.num = -1
        
        self.blockSd = False
       
        self.butonToReset = self.button2
 
        self.setup()

    def setup(self,reset=False):
        for led in self.leds:
            GPIO.setup(led, GPIO.OUT)

        self.reset()
        GPIO.setup(self.button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.setup(self.button2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.button2, GPIO.RISING, callback=self.resetPress, bouncetime=200)

        GPIO.setup(self.button3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.button3, GPIO.RISING, callback=self.changeSecuence, bouncetime=200)

    def changeButons(self,b1):

        if b1 == 1:
            if self.butonToReset != self.button2:
                print "button 2 para reset"
                GPIO.remove_event_detect(self.button1)
                GPIO.remove_event_detect(self.button2)
                GPIO.add_event_detect(self.button1, GPIO.RISING, callback=self.next, bouncetime=200)
                GPIO.add_event_detect(self.button2, GPIO.RISING, callback=self.resetPress, bouncetime=200)
                self.butonToReset = self.button2
                
        else:
            if self.butonToReset != self.button1:
                print "button 1 para reset"
                GPIO.remove_event_detect(self.button1)
                GPIO.remove_event_detect(self.button2)
                GPIO.add_event_detect(self.button2, GPIO.RISING, callback=self.next, bouncetime=200)
                GPIO.add_event_detect(self.button1, GPIO.RISING, callback=self.resetPress, bouncetime=200)
                self.butonToReset = self.button1

    def reset(self):
        for led in self.leds:
            GPIO.output(led,False)


    def output(self):
        print "ejecutando la secuencia:",self.num
        if self.num == -1:
            return 1
        select = self.sec[self.num]
        while 1:
            for sec in select:
                if self.restoreState:
                    return 1
                for i,val in enumerate(sec):
                    GPIO.output(self.leds[i],val)
                for i in range(self.pause*2):
                    if self.restoreState:
                        return 1
                    sleep(1)
            self.reset()
            sleep(.002)

    def nextBack(self,v):
        print "vvvv-----",v
        if self.restoreState == True:
            return 1
        self.restoreState = True
        self.reset()
        n = self.num + 1
        l = len(self.sec)
        self.num = n % l
        #sleep(1)
        self.restoreState = False
        print "Siguiente secuencia : ",self.num
        #self.output()

    def next(self,v):
        logger.info("next")
        print "-------------"
        self.reset()
        self.stop = True
        sleep(.5)

        n = self.num + 1
        l = len(self.sec)
        self.num = n % l
        self.stop = False

        select = self.sec[self.num]
        print 'select',self.num
        logger.info("sec: "+str(self.num))

        while 1:

            for sec in select:
                if self.stop:
                    return
                for i,val in enumerate(sec):
                    GPIO.output(self.leds[i],val)
                #sleep(self.pause)
                for i in range(self.pause*10):
                    if self.stop:
                        return
                    sleep(.1)
            self.reset()
            sleep(.01)


    def resetPress(self,v):
	logger.info("reset")
        print "pressss! reset"
        self.stop = True
        self.reset()

    def getSdDataRaw(self):
        bashCommand = "./sdCard"
        if not self.blockSd:
            self.blockSd = True
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE,cwd="/home/pi/sd2/sdcard/inOut/")
            output = process.communicate()[0]
            output = output.strip()
            self.blockSd = False
            return output
        return "0"

    def getSdData(self):
        #data = "b2 stop\nb1 1 0 0 0 0 1 0 0 1 1 0 0 1, 1 0 1 0 1 0 0"
        #return data
        print "button press"
        m = 0
        while 1:
            res = self.getSdDataRaw()
            if res != "0" or m == 3:
                break 
            m +=1
        return res    

    def getValueOption(self,string,index):
        if "stop" in string:
            return index
        else:
            secuencias = []
            secuencia = []
            string = string.strip()
            if string[-1] != ',':
                string += ','
            for x in string:
                
                if x != " ":
                    if x == "0":
                        secuencia.append(False)
                    elif x == ",":
                        res = []
                        for i in range(0,len(secuencia),6):
                            s = []
                            for j in range(0,6):
                                if i+j < len(secuencia):
                                    s.append(secuencia[i+j])
                                else:
                                    s.append(False)

                            res.append(s)
                        secuencias.append(res)
                        secuencia = []
                    else:
                        secuencia.append(True)
                
                

            return secuencias 
        
        return False

    def parseSdData(self,data):
        #data = "b1 1 1 0 0 1 1\nb2 stop" 
        
        d = data.split("\n")
        if not len(d) >= 2:
            print "no 2"
            return False
        b1 = False
        b2 = False
        res = []
        for i in range(2):
            if d[i][0] != "b":
                print "no b,",d[i][0]
                return False
            if d[i][1] == "1":
                b1 = True
                res.append(self.getValueOption(d[i][3:],0))
            elif d[i][1] == "2": 
                res.append(self.getValueOption(d[i][3:],1))
                b2 = True
            else:
                return False
        if not b1 or not b2:
            return False    
    
        return res

    def changeSecuence(self,v):
	logger.info("change sec")
        print "life!"
        self.resetPress(v)
        sleep(.06)
        self.allLeds(True)
        data = self.getSdData()
        res = self.parseSdData(data)
        print "res",res
        success = False
        if res and len(res) == 2:
            index = -1
            if res[0] == 0 or res[0] == 1:
                index = res[0]
                sec = res[1]
            else:
                index = res[1]
                sec = res[0]
            if index != -1:
                self.sec = sec
                self.changeButons(index)
                success = True
            """
            if res[0] != 0:#buton 1 sec, b2 reset
                print "change, reset 2"
                self.sec = res[0]
                self.changeButons(1)
                success = True
                for i in res[0]:
                    print '---------------'
                    for j in i:
                            print j
            else:
                print "change, reset 1"
                self.sec = res[1]
                self.changeButons(2)
                success = True
            """
        self.allLeds(False)
        if success:
            self.num = -1
            self.next(1)
    
    def allLeds(self,to):
        for i in self.leds:
            GPIO.output(i,to)

if __name__ == '__main__':
    logger.info("run")
    try:

        t = Secuence(1)
        GPIO.add_event_detect(t.button1, GPIO.RISING, callback=t.next, bouncetime=200)
        t.changeSecuence(1)#leemos la primera sec.
        while 1:
            sleep(0.2)
        #GPIO.cleanup()
        #print 'clear'

    except KeyboardInterrupt,e:
        print str(e)
        GPIO.cleanup()
        print 'clear'
