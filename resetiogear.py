# Resets iogear print servers as specified in arguments
# Thomas McLean 2022

import sys
import time
import telnetlib

def prepareHostString(host_string, selection):
    host_string = host_string.split(',')[selection].strip()
    if host_string.startswith('\'') and host_string.endswith('\''):
        prepared_string = host_string[1:-1]

    return prepared_string

def logOutput(output_string):
    open_file = open('IOGearLogfile.log', 'a')
    open_file.write("\n" + output_string)

    open_file.close()

def checkIOgearStatus(arglength, argcontent):
    content = str(argcontent)[1:-1]
    connections = 1
    while (connections < arglength):
        p_host = prepareHostString(content, connections)
        print(p_host.encode('utf-8'))

        tel = telnetlib.Telnet(p_host.encode('utf-8'))
        print ("Logging onto device")
        tel.read_until('Password:'.encode('utf-8'))
        tel.write('\r\n'.encode('utf-8'))

        print ("Querying print server status")
        tel.read_until('->'.encode('utf-8'))
        tel.write('1\r\n'.encode('utf-8'))

        print ("Querying connected printers")
        tel.read_until('->'.encode('utf-8'))
        tel.write('2\r\n'.encode('utf-8'))

        print ("Getting printer status")
        time.sleep(5)
        log_txt = tel.read_very_eager()
        print (log_txt)

        tel.close()
        connections += 1

        
# Take a list of connections, step through them, and input commands
def resetIOgear(arglength, argcontent):
    content = str(argcontent)[1:-1]
    connections = 1
    while (connections < arglength):
        p_host = prepareHostString(content, connections)
        print(p_host.encode('utf-8'))

        tel = telnetlib.Telnet(p_host.encode('utf-8'))
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


def selectFunction(function_string, arglength, argcontent):

    if (function_string is "/reset" or function_string is "/r"):
        resetIOgear(arglength, argcontent)
    elif (function_string is "/check" or function_string is "/c"):
        checkIOgearStatus(arglength, argcontent)
    else:
        print ("No function given\nUsage: function ip1 ip2 ip...\nAvalable functions are /reset and /check")



# Pass command line arguments to function
# resetIOgear(len(sys.argv), str(sys.argv))
# checkIOgearStatus(len(sys.argv), str(sys.argv))