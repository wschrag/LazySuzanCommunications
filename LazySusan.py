##### Extrenal module
import numpy as np
import sys
import RPi.GPIO as GPIO
import threading
import collections
from bitstream import BitStream
###  Pin Declartions and Settings #####
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()
outputwire = 33
inputwire= 31
Ackin = 36
Ackout = 37
Thandshakein = 29
Thandshakeout = 32

### global-scoped vars ###
sender = None
reciever = None
senderID = BitStream()
recieverID = BitStream()
inputframe = BitStream()
outStream = BitStream()
inputStr = ''
sender = BitStream()
currentBit = 0
isSending = None

GPIO.setup(outputwire, GPIO.OUT)
GPIO.setup(inputwire, GPIO.IN)
GPIO.setup(Ackin, GPIO.IN)
GPIO.setup(Ackout, GPIO.OUT)
GPIO.setup(Thandshakein, GPIO.IN)
GPIO.setup(Thandshakeout, GPIO.OUT)
GPIO.setwarnings(False)

GPIO.add_event_detect(Ackin, GPIO.BOTH, callback=ackin_callback, bouncetime=10)
###### input and output threads ######

nodeID = sys.argv[1]

inQueue = collections.deque()
outQueue = collections.deque()



def consoleInput():
    while(True):
        consoleIn = raw_input()
        if(consoleIn == 'start'):
            print('starting token ring')
            outMessage = "000"
            send_message(outMessage)
        inQueue.appendleft(consoleIn)

def consoleOutput():
    while(True):
        if(len(outQueue) != 0):
            consoleOut = outQueue.pop()
            print(consoleOut)

def sending_state():
    while(True):
        if(isSending != None):
            if(isSending):
                print('THSout is now input')
                GPIO.setup(Thandshakeout, GPIO.IN)
                GPIO.add_event_detect(Thandshakeout, GPIO.BOTH, callback=send_bit, bouncetime=10)
            else:
                GPIO.remove_event_detect(Thandshakeout)
                GPIO.setup(Thandshakeout, GPIO.OUT)

def reading_state():
    while(True):
        if(isSending != None):
            if(not isSending):
                print('THSin is now input')
                GPIO.setup(Thandshakein, GPIO.IN)
                GPIO.add_event_detect(Thandshakein, GPIO.BOTH, callback=read_bit, bouncetime=10)
            else:
                GPIO.remove_event_detect(Thandshakein)
                GPIO.setup(Thandshakein, GPIO.OUT)


### Resetting values that need to be reset ###
def reset_sender_reciever():
    sender = None
    reciever = None
    currentBit = 0

### Reading message logic ###
def flip_bit(gpio_id):
    if(GPIO.input(gpio_id)):
        GPIO.output(gpio_id, GPIO.LOW)
    else:
        GPIO.output(gpio_id, GPIO.HIGH)   

def ackin_callback(gpio_id):
    print('ackin flip')
    if(GPIO.input(Ackin)):
        read_message()
    

def read_message():
    isSending = False
    print('isSending is: ')
    print(isSending)
    sender = senderID.read(np.uint8, 1)
    print('Sender is: ')
    print(sender)
    reciever = recieverID.read(np.uint8, 1)
    print('Reciever is: ')
    print(reciever)
    while((inputframe // 8) != 0):
        inputStr = inputStr + inputframe.read(str, 1)
    print("inputStr is: ")
    print(inputStr)
    parse_message(sender, reciever, inputStr)

### Parsing and Writing Message Logic ###
def parse_message(sender, reciever, message):
    print(message)
    
    #first check to see if message is meant for this node
    if(reciever == nodeID):
        outQueue.appendLeft(message)
        outMessage = "000"
        reset_sender_reciever()
        send_message(outMessage)
        
    #then check to see if message is empty, by checking if sender or reciever is 0
    elif((sender == 0) or (reciever == 0)):
        outMessage = None
        if(len(inQueue) != 0):
            outMessage = inQueue.pop()
        
        reset_sender_reciever()
        send_message(outMessage)

def send_message(message):
    print("Sending Message: ")
    print(message)
    isSending = True
    GPIO.output(Ackout, GPIO.HIGH)
    print(Ackout)
    #now to form output bitstream message
    outStream.write(message, str)
    print(outStream)
    send_bit(outputwire)

def finish_message():
    isSending = False
    #send ack to let reciever know message is now done
    GPIO.output(Ackout, GPIO.LOW)

### Reading and Sending Bits ###
def read_bit(gpio_id):
    if(not isSending):
        #logic for reading a bit
        writeVal = GPIO.input(inputwire)
        if(GPIO.input(Ackin)):
            if(currentBit < 8):
                senderID.write(writeVal, bool)
            elif(currentBit < 16):
                recieverID.write(writeVal, bool)
            else:
                inputframe.write(writeVal, bool)

            currentBit = currentBit + 1
            flip_bit(Thandshakein)

def send_bit(gpio_id):
    #now the logic for sending the message via outputWire and Thandshakeout bit by bit
    print(len(outStream))
    if(outStream.read(bool, 1)):
        GPIO.output(outputwire, GPIO.HIGH)
    else:
        GPIO.output(outputwire, GPIO.LOW)

    flip_bit(Thandshakeout)

    if(len(outStream) == 0):
        finish_message()


### Starting input and output threads ###
inputThread = threading.Thread(target=consoleInput, args=())
outputThread = threading.Thread(target=consoleOutput, args=())
sendThread = threading.Thread(target=sending_state, args=())
readThread = threading.Thread(target=reading_state, args=())
inputThread.start()
outputThread.start()
sendThread.start()
readThread.start()

### Adding Callbacks ###
#GPIO.add_event_detect(Thandshakein, GPIO.BOTH, callback=read_bit, bouncetime=10) #default edge is both
#GPIO.add_event_detect(Thandshakeout, GPIO.BOTH, callback=send_bit, bouncetime=10) #default edge is both again
