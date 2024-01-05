# Brian Lesko
# Arduino Nano Esp 32 - Micropython
# https://docs.arduino.cc/micropython-course/course/introduction-python
# 12/2023

import machine 
from machine import Pin, PWM, ADC
import network
import socket
import time

class nano:

    def __init__(self):
        self.log = []
        self.wlan = network.WLAN(network.STA_IF) # Connect to wifi 
        # Networking
        self.IP = None
        self.client_address = None 
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

    def do_connect(self):
        if self.wlan.isconnected() == False:
            self.log_and_serial_send("Attempting to connect to wifi")
            self.wlan.active(True)
            if not self.wlan.isconnected():
                SSID = 'network_name'
                self.wlan.connect(SSID, 'password')
                start_time = time.time()  # Record the start time
                timeout = 5  # Set the timeout duration in seconds
                while not self.wlan.isconnected():
                    if time.time() - start_time > timeout:
                        break
            if self.wlan.isconnected():
                self.log_and_serial_send(f'Successfully connected to {SSID}')
            else:
                self.log_and_serial_send('Failed to connect within the timeout period')
            return self.wlan
        if self.wlan.isconnected() == True:
            self.IP = str(self.wlan.ifconfig()[0])
            self.server.bind((self.IP, 12345))
        
    def log_and_serial_send(self, message):
        self.log.append(message)
        #self.serial_send(message)

nno = nano()
pwmPin = PWM(Pin(2))
myLED = Pin(9, Pin.OUT)
dirPin = Pin(1, Pin.OUT)
dirPin.value(1)

while True:
    steps = 0
    nno.do_connect()
    try: 
        data, addr = nno.server.recvfrom(1024) # buffer size is 1024 bytes
        steps = int(round(float(data),0))
        print("received message: %s" % steps)
    except: continue
        
    
    
    
