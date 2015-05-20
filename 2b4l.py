from time import sleep
import RPi.GPIO as GPIO
import threading
GPIO.setmode(GPIO.BOARD)


def test(led):
    GPIO.setup(led, GPIO.OUT)
    while 1:
        GPIO.output(led,True)
        sleep(1)
        GPIO.output(led,False)
        sleep(1)

def testButton(pin):
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    while 1:
        if GPIO.input(pin) == 1:
            print "Button press"

        sleep(.02)

def callbackButtonEvent(pin):
    print "button press"

def testButtonEvent(pin):
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=callbackButtonEvent, bouncetime=300)


class Secuence(object):

    def __init__(self,pause=1):

        self.sec = [
            [#secuencia 1
                [False,True,False,True],
                [True,False,True,False]
            ],
            [
                [True,False,False,False],
                [False,True,False,False],
                [False,False,True,False],
                [False,False,False,True]
            ],
            [
                [False,True,True,False],
                [True,False,False,True]
            ]
        ]

        self.restoreState = False

        self.leds = [26,24,22,16]
        self.pause = pause

        self.button1 = 12
        self.button2 = 10

        self.num = -1


        self.setup()

    def setup(self):
        for led in self.leds:
            GPIO.setup(led, GPIO.OUT)

        self.reset()
        GPIO.setup(self.button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.setup(self.button2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.button2, GPIO.RISING, callback=self.resetPress, bouncetime=200)

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
        print "pressss! reset"
        self.stop = True
        self.reset()


if __name__ == '__main__':
    #pin = 26
    #pin = 24
    #pin = 22
    #pin = 16
    try:
        #test(pin)
        #testButtonEvent(12)
        #testButtonEvent(10)
        t = Secuence(1)
        GPIO.add_event_detect(t.button1, GPIO.RISING, callback=t.next, bouncetime=200)

        raw_input()
        GPIO.cleanup()

    except KeyboardInterrupt,e:
        print str(e)
        GPIO.cleanup()
        print 'clear'
