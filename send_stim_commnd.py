#
# send_stim_command.py
#
# Input parameters:  channel, unit, protocol
# Output: Send command over serial ports (& stdio/log for debug) to the stim units
#

# For BBB serial port access
#import Adafruit_BBIO.UART as UART
#import serial

import logging


# Test Variables <-- In the real code, we would get this from app.py (flask)
_channel = 1
_address = 0		# broadcast
_protocol = 1

invalid_chars = set('23456789') 	# invalid characters for address field

# Define valid command set
valid_commands = map(chr, xrange(65,77))	# list of valid command letters (A - L)
valid_commands.insert(0, "0")				#    and number '0'

# Setup logging

# add filemode="w" to overwrite log
logging.basicConfig(filename="stim_command.log", level=logging.INFO)
log = logging.getLogger("ex")
logging.info("Logger enabled for send_stim_command.py")


# Setup Serial UARTs
try:
    UART.setup("UART1")
    logging.info("Set up 1 serial port, UART1")
except Exception, err:
    log.exception("Error! UART1 not available")


####################################################################################
#
# Instructions:
# - Interface with serial port via helper functions.  
#   These will do data validation & high-order logging
#
# - Helper functions will transmit fata via centralized 'send_command' function
#
####################################################################################

# HELPER FUNCTIONS

# set port command code + <port[0,1]> + <0 | 1> 
def setPort(address,port,enable1_disable0):
	if not validateAddress(address):
		if port < 2 and port >= 0:
		    logging.info("Set Port command: address=" + address + " / port=" +port+ " / value=" + enable1_disable0)
			send_command(addressB1=address, commandB1="B", param1B1=port, param2B1=enable1_disable0)
		else:
		    logging.warning("Set Port command: Incorrect port # received.  Command not sent.)
			print("Invalid parameters")



# MAIN SENDING FUNCTION
# Send command using frame format on 'channel'
#
# - trailing B# = # bytes in the paramter
def send_command(channel, addressB1,commandB1,param1B1,param2B1,valueB4="    "):
    # Determine which serial port to use.
    serial_port_choices = {1: serial_port1, 2: serial_port2, 3: serial_port3, 4: serial_port4}	
    serial_port = serial_port_choices.get(channel, serial_port1) 	# serial_port1 (here) is the default if key not found.
    
    # Transmit data packet
    # - Validate that connection is available
    #try:
    serial_port.write(addressB1 + commandB1 + param1B1 + param2B1 + valueB4)
    # [ ] How do we get ACK / NACK?
    # [ ] How do we want to track, if needed?

# Return value: -1 = fail; 0 = pass
# Python does not support a character type; these are treated as strings of length one
def validateAddress (address):
    # Make sure that the address field fits the format as specified (length = 1 byte)
    if len(address.encode("utf8")) == 1:
        # Valid address length
        # Check for any invalid addresses (invalid characters)
        if any((c in invalid_chars) for c in address):
            print('Invalid Address')
            return -1
        else:
            print('Address is valies')
            return 0
    else:
        print('Incorrect address length')
        return -1

def validateCommand (command):
	if len(address.encode("utf8")) == 1:
		# Valid address length
		
		# Check if command given is valid
		if command in valid_commands:
			print("Valid command received")
			return 0
		else:
			print("Invalid command received")
			return -1
	else:
		print('Incorrect address length')
		return -1
		

# Code for sending command to the serial port
# serial_port1 = serial.Serial(port = "/dev/ttyO1", baudrate=9600)
# ser.close()
# ser.open()
# if ser.isOpen():
# 	print "Serial is open!"
#     ser.write("Hello World!")
# ser.close()

# Eventually, you'll want to clean up, but leave this commented for now, 
# as it doesn't work yet
#UART.cleanup()
