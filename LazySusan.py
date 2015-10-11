##### Extrenal module
import time
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
bitLocation = 0
isSending = False

GPIO.setup(outputwire, GPIO.OUT)
GPIO.setup(inputwire, GPIO.IN)
GPIO.setup(Ackin, GPIO.IN)
GPIO.setup(Ackout, GPIO.OUT)
GPIO.setup(Thandshakein, GPIO.IN)
GPIO.setup(Thandshakeout, GPIO.OUT)
GPIO.setwarnings(False)

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


### Resetting values that need to be reset ###
def reset_sender_reciever():
    global sender
    global reciever
    global bitLocation
    sender = None
    reciever = None
    bitLocation = 0

### Reading message logic ###
def flip_bit(gpio_id):
    GPIO.setup(gpio_id, GPIO.OUT)

    if(GPIO.input(gpio_id) == GPIO.HIGH):
        GPIO.output(gpio_id, GPIO.LOW)
    else:
        GPIO.output(gpio_id, GPIO.HIGH)   

    GPIO.setup(gpio_id, GPIO.IN)

def ackin_callback(gpio_id):
    if(GPIO.input(Ackin)):
        print('ackin flip')
        print(GPIO.input(Ackin))
        read_bit(inputwire)
    else:
        read_message()    

def read_message():
    global inputStr
    global inputframe
    #setup reading state
    print('THSin is now input')
    GPIO.setup(Thandshakein, GPIO.IN)
    GPIO.remove_event_detect(Thandshakein)
    #GPIO.add_event_detect(Thandshakein, GPIO.BOTH, callback=read_bit, bouncetime=100)
    print('THSout is now output')
    #GPIO.remove_event_detect(Thandshakeout)
    GPIO.setup(Thandshakeout, GPIO.OUT)
    
    isSending = False
    print('isSending is: ')
    print(isSending)
    sender = senderID.read(np.uint8, 1)
    print('Sender is: ')
    print(sender)
    reciever = recieverID.read(np.uint8, 1)
    print('Reciever is: ')
    print(reciever)
    while((len(inputframe) // 8) != 0):
        inputStr = inputStr + inputframe.read(str, 1)
    print("inputStr is: ")
    print(inputStr)
    parse_message(sender, reciever, inputStr)

### Parsing and Writing Message Logic ###
def parse_message(sender, reciever, message):
    global inQueue
    print(message)
    
    #first check to see if message is meant for this node
    if(reciever == nodeID):
        outQueue.appendLeft(message)
        outMessage = "000"
        reset_sender_reciever()
        send_message(outMessage)
        
    #then check to see if message is empty, by checking if sender or reciever is 0
    elif((sender == 0) or (reciever == 0)):
        outMessage = ''
        if(len(inQueue) != 0):
            outMessage = inQueue.pop()
        else:
            outMessage = "000"
        
        reset_sender_reciever()
        send_message(outMessage)
    else:
        send_message(message)

def send_message(message):
    #setup sending state
    print('THSout is now input')
    GPIO.setup(Thandshakeout, GPIO.IN)
    GPIO.add_event_detect(Thandshakeout, GPIO.BOTH, callback=send_bit, bouncetime=150)
    print('THSin is now output')
    GPIO.remove_event_detect(Thandshakein)
    GPIO.setup(Thandshakein, GPIO.OUT)


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
    #go back into reading state


### Reading and Sending Bits ###
def read_bit(gpio_id):
    if(GPIO.input(Ackin) == GPIO.HIGH):
        global bitLocation
        currentVal = bitLocation

        #logic for reading a bit
        writeVal = GPIO.input(inputwire)
        print(writeVal)
        if(currentVal < 8):
            senderID.write(writeVal, bool)
        elif(currentVal < 16):
            recieverID.write(writeVal, bool)
        else:
            inputframe.write(writeVal, bool)

        currentVal = currentVal + 1
        bitLocation = currentVal

        GPIO.remove_event_detect(Thandshakein)
        flip_bit(Thandshakein)
        time.sleep(0.250)
        GPIO.add_event_detect(Thandshakein, GPIO.BOTH, callback=read_bit, bouncetime=150)
    else:
        GPIO.remove_event_detect(Thandshakein)

def send_bit(gpio_id):
    if((len(outStream)) == 0):
        print('outStream == 0 now')
        GPIO.remove_event_detect(Thandshakeout)
        finish_message()
        return

    #now the logic for sending the message via outputWire and Thandshakeout bit by bit
    print(len(outStream))
    if(outStream.read(bool, 1) == [True]):
        GPIO.output(outputwire, GPIO.HIGH)
    else:
        GPIO.output(outputwire, GPIO.LOW)
    
    print('flipping THSout after sending bit')
    GPIO.remove_event_detect(Thandshakeout)
    flip_bit(Thandshakeout)
    time.sleep(0.250)
    GPIO.add_event_detect(Thandshakeout, GPIO.BOTH, callback=send_bit, bouncetime=150)

### Starting input and output threads ###
inputThread = threading.Thread(target=consoleInput, args=())
outputThread = threading.Thread(target=consoleOutput, args=())
#sendThread = threading.Thread(target=sending_state, args=())
#readThread = threading.Thread(target=reading_state, args=())
inputThread.start()
outputThread.start()
#sendThread.start()
#readThread.start()

### Adding Callbacks ###
GPIO.add_event_detect(Ackin, GPIO.BOTH, callback=ackin_callback, bouncetime=150)
GPIO.add_event_detect(Thandshakein, GPIO.BOTH, callback=read_bit) #default edge is both
#GPIO.add_event_detect(Thandshakeout, GPIO.BOTH, callback=send_bit, bouncetime=100) #default edge is both again
