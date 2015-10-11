##### Extrenal module
import sys
import RPIO
import threading
import collections
from bitstream import BitStream
###  Pin Declartions and Settings #####
RPIO.setmode(RPIO.BOARD)
outputwire = 33
inputwire= 31
Ackin = 36
Ackout = 37
Thandshakein = 29
Thandshakeout = 32

RPIO.setup(outputwire, RPIO.OUT)
RPIO.setup(inputwire, RPIO.IN)
RPIO.setup(Ackin, RPIO.IN)
RPIO.setup(Ackout, RPIO.OUT)
RPIO.setup(Thandshakein, RPIO.IN)
RPIO.setup(Thandshakeout, RPIO.OUT)
RPIO.setwarnings(False)
###### input and output threads ######

nodeID = sys.argv[1]

inQueue = collections.deque()
outQueue = collections.deque()

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
isSending = False


def consoleInput():
    while(True):
        consoleIn = raw_input()
        if(consoleIn == 'start'):
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
    sender = None
    reciever = None
    currentBit = 0

### Reading message logic ###
def flip_bit(gpio_id):
    if(RPIO.input(gpio_id)):
        RPIO.output(gpio_id, RPIO.LOW)
    else:
        RPIO.output(gpio_id, RPIO.HIGH)

def read_bit(gpio_id, val):
    writeVal = RPIO.input(inputwire)
    if(RPIO.input(Ackin)):
        if(currentBit < 8):
            senderID.write(writeVal, bool)
        elif(currentBit < 16):
            recieverID.write(writeVal, bool)
        else:
            inputframe.write(writeVal, bool)

        currentBit = currentBit + 1
        flip_bit(Thandshakeout)
        

def ackin_callback_falling(gpio_id, val):
    read_message()

def read_message():
    sender = senderID.read(uint8, 1)
    reciever = recieverID.read(uint8, 1)
    while((inputframe // 8) != 0):
        inputStr = inputStr + inputframe.read(str, 1)
    parse_message(sender, reciever, inputStr)

### Parsing and Writing Message Logic ###
def parse_message(sender, reciever, message):
    
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
    #
    isSending = True
    RPIO.output(Ackout, RPIO.HIGH)
    #now to form output bitstream message
    outStream.write(message, str)

def send_bit(gpio_id, val):
    if(isSending):
        #now the logic for sending the message via outputWire and Thandshakeout bit by bit
        print(len(outStream))
        if(outStream.read(bool, 1)):
            RPIO.output(outputwire, RPIO.HIGH)
        else:
            RPIO.output(outputwire, RPIO.LOW)

        flip_bit(Thandshakeout)

        if(len(outStream) == 0):
            finish_message()

def finish_message():
    isSending = False
    #send ack to let reciever know message is now done
    RPIO.output(Ackout, RPIO.LOW)


### Starting input and output threads ###
inputThread = threading.Thread(target=consoleInput, args=())
outputThread = threading.Thread(target=consoleOutput, args=())
inputThread.start()
outputThread.start()

### Adding Callbacks ###
RPIO.add_interrupt_callback(Ackin, ackin_callback_falling, edge='falling', debounce_timeout_ms=10)
RPIO.add_interrupt_callback(Thandshakein, read_bit) #default edge is both
RPIO.add_interrupt_callback(Thandshakein, send_bit) #default edge is both again
RPIO.wait_for_interrupts()
