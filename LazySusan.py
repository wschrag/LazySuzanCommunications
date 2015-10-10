##### Extrenal module
import RPi.GPIO as GPIO
import threading
import collections.deque
###  Pin Declartions #####
outputwire = 33
inputwire= 31
Ackin = 36
AckOut = 37
Thandshakein = 29
Thandshakeout = 32
###### input and output threads ######

inQueue = collections.deque()
outQueue = collections.deque()


def consoleInput():
    while(True):
        consoleIn = raw_input()
        inQueue.appendleft(consoleIn)

def consoleOutput():
    while(True):
        if(len(outQueue) != 0):
            consoleOut = outQueue.pop()
            print(consoleOut)

def tokenRing():
    ######  inputs ######
    inputframe = raw_input
    sender = raw_input
    ######  sets ######
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(inputwire, GPIO.IN)
    GPIO.setup(outputwire, GPIO.OUT)
    GPIO.setup(Ackin, GPID.Ackin)
    GPIO.setup(Ackout, GPIO.Ackout)
    GPIO.setup(thandshakein, GPIO.THSin)
    GPIO.setup(thandshakeout, GPIO.THSout)
    ######## methods  #######
    def __reciever__(message):
        if (sender == sender ):
            print( reciever(message))
        elif(sender == null):
        else:
            for (i in range Ackin.high):
                while(TSHin)

    for (i in range Ackin.high)
        print (i)
        while (thandShakein.high= True ):
            print (foo)
            sleep.time(2)
                if (messager = True):
                    print(mass)
                    framebuffer = inputframe ##  this will take the input in the end

inputThread = threading.Thread(target=consoleInput, args=())
outputThread = threading.Thread(target=consoleOutput, args())
tokenRingThread = threading.Thread(target=tokenRing, args())
inputThread.start()
outputThread.start()
tokenRingThread.start()

