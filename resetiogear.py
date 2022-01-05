# Resets iogear print servers as specified in arguments
# Thomas McLean 2022

import sys
import telnetlib

# Take a list of connections, step through them, and input commands
def resetIOgear(arglength, argcontent):
    content = str(argcontent)[1:-1]
    connections = 1
    while (connections < arglength):
        tel = telnetlib.Telnet(content.split(',')[connections], 23, 3)
        tel.read_until("Password: ")
        tel.write("\n")

        tel.read_until("-> ")
        tel.write("4\n")

        tel.read_until("(Y/N) ")
        tel.write("Y")
        connections += 1


# Pass command line arguments to function
resetIOgear(len(sys.argv), str(sys.argv))

      