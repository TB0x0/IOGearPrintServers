# Resets iogear print servers as specified in arguments
# Thomas McLean 2022

import sys
import telnetlib

# Take a list of connections, step through them, and input commands
def resetIOgear(arglength, argcontent):
    content = str(argcontent)[1:-1]
    connections = 1
    while (connections < arglength):
        current_host = content.split(',')[connections]
        tel = telnetlib.Telnet(current_host.encode('utf-8'))
        print ("Logging onto device")
        tel.read_until('Password:'.encode('utf-8'))
        tel.write('\r\n'.encode('utf-8'))
        
        print ("Resetting Device")
        tel.read_until('->'.encode('utf-8'))
        tel.write('4\r\n'.encode('utf-8'))

        tel.read_until('N)'.encode('utf-8'))
        tel.write('Y\r\n'.encode('utf-8'))

        print ("Device Reset Complete")
        connections += 1


# Pass command line arguments to function
resetIOgear(len(sys.argv), str(sys.argv))

