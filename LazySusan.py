##### Extrenal module
import RPIO
import threading
import collections.deque
from bitstream import BitStream
###  Pin Declartions and Settings #####
RPIO.setmode(RPIO.BOARD)
outputwire = 33
inputwire= 31
Ackin = 36
Ackout = 37
Thandshakein = 29
Thandshakeout = 32

RPIO.setup(outputWire, RPIO.OUT)
RPIO.setup(inputWire, RPIO.IN)
RPIO.setup(Ackin, RPIO.IN)
RPIO.setup(Ackout, RPIO.OUT)
RPIO.setup(Thandshakein, RPIO.IN)
RPIO.setup(Thandshakeout, RPIO.OUT)
###### input and output threads ######

nodeID = sys.argv[1]

inQueue = collections.deque()
outQueue = collections.deque()

### global vars ###
sender = None
reciever = None
senderID = BitStream()
recieverID = BitStream()
inputframe = BitStream()
inputStr = ''
sender = BitStream()


def consoleInput():
    while(True):
        consoleIn = raw_input()
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

### Reading message logic ###
def flip_bit(gpio_id):
    if(RPIO.input(gpio_id)):
        RPIO.output(gpio_id, RPIO.LOW)
    else:
        RPIO.output(gpio_id, RPIO.HIGH)

def read_bit(gpio_id, val):
    currentBit = 0
    if(RPIO.input(Ackin)):
        if(currentBit < 8):
            senderID.write(val, bool)
        elif(currentBit < 16):
            recieverID.write(val, bool)
        else:
            inputframe.write(val, bool)

        currentBit = currentBit + 1
        flip_bit(Thandshakeout)
    else:
        currentBit = 0

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
    RPIO.output(Ackout, RPIO.HIGH)
    #now to form output bitstream message
    outStream = BitStream()
    outStream.write(message, str)

    #now the logic for sending the message via outputWire and Thandshakeout
    while(len(outStream) != 0):
        RPIO.output(outputWire, outStream.read(bool, 1))
        flip_bit(Thandshakeout)

    RPIO.output(Ackout, RPIO.LOW)

### Starting input and output threads ###
inputThread = threading.Thread(target=consoleInput, args=())
outputThread = threading.Thread(target=consoleOutput, args())
inputThread.start()
outputThread.start()

### Adding Callbacks ###
RPIO.add_interrupt_callback(Ackin, ackin_callback_rising, edge='rising')
RPIO.add_interrupt_callback(Ackin, ackin_callback_falling, edge='falling')
RPIO.add_interrupt_callback(Thandshakein, read_bit) #default edge is both
RPIO.wait_for_interrupts()
