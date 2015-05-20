import subprocess
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
#LED_BLOCK = 18
LED_BLOCK = 16
LED_BLOCK = 12
LED_BLOCK = 10
LED_BLOCK = 7
LED_BLOCK = 8
GPIO.setup(LED_BLOCK, GPIO.OUT)

bashCommand = "./sdCard"
block = False
def getSdData():
    global block
    if not block:
        block = True
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        output = output.strip()
        block = False
        return output
    return "0"

def blockSd():
    global LED_BLOCK
    GPIO.output(LED_BLOCK,True)

def unBlockSd():
    global LED_BLOCK
    GPIO.output(LED_BLOCK,False)
    

def buttonChangeData(pin):
    print "button press"
    m = 0
    while 1:
        print "wait"
        blockSd()
        res = getSdData()
        print "continue"
        unBlockSd()
        if res != "0" or m == 3:
            break
        
        m +=1
        
    print "data read",res    
 
def testButtonEvent(pin):
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=buttonChangeData, bouncetime=9500)

if __name__=="__main__":
    unBlockSd()
    #testButtonEvent(15)
    #testButtonEvent(11)
    testButtonEvent(5)
    print "test" 
    try:
        raw_input()
    except KeyboardInterrupt,e:
        GPIO.cleanup()
        print "clear"
