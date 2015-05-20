import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

leds = [18,16,12,10,8,11]
for i in leds:
    GPIO.setup(i, GPIO.OUT)

for i in leds:
    GPIO.output(i,False)
    GPIO.output(i,True)

def buttonChangeData(pin):
    print pin

def testButtonEvent(pin):
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=buttonChangeData, bouncetime=1500)

if __name__ == "__main__":
    testButtonEvent(13)
    testButtonEvent(15)
    testButtonEvent(7)
    print "test" 
    try:
        raw_input()
    except KeyboardInterrupt,e:
        GPIO.cleanup()
        print "clear"
