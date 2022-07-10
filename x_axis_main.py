"""
esp_now_listen.py
Starting point for developing axis controller software.

Recieves a msg from another esp and displays it. This is part of the initial
test to get a message from Rpi over its serial comm to an attached
esp32 that is the Marshaller. If the message is something for one of the
axis controllers, it sends the message on over esp-now.
To use the file, save it as main.py on an axis controller esp32 
"""
import network
from esp import espnow
import time

peer1 = b'\x08\x3a\xf2\x86\x69\x74'
peer2 = b'\x3c\x61\x05\x4b\x0c\xf8'
marshaller = b'\xc4\xdd\x57\xb8\xe8\xe8'

#Stop when done.
end = False
message_count = 0
start_time = time.ticks_ms()

def to_mac_string( bytes ):
   
    mac_string = ""
    for b in bytes:
        mac_string += hex(b)
    newStr = mac_string.replace('0x', ':')
    rtnStr = newStr.lstrip(':')
   
    return rtnStr

def receive_callback(e):
    global end
    global message_count
    host, msg = e.irecv()
    if msg:
        message_count = message_count+1
        print(to_mac_string(host), msg)
        if msg == b'end':
            end = True



#A WLAN interface must be active to send/recv
w0 = network.WLAN(network.STA_IF)
w0.active(True)

e = espnow.ESPNow()
e.init()
e.config(on_recv=receive_callback)
e.add_peer(marshaller)


   
 
print('done with setup, now listen')

while True:
   
    current_time = time.ticks_ms()
    time_diff = time.ticks_diff(current_time, start_time)
   
    if time_diff >= 20000 or time_diff <= 0:
        end = True
       
    if end:
        print(f"Time diff: {time_diff}, Messsage count: {message_count}")
        break


 