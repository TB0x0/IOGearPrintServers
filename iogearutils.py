# Manages IOGear print servers using terminal or command line
# Thomas McLean 2022

import socket
import sys
import time
import telnetlib

# Cut the array down, grab the selection, and give only the string without any extra quotes
def prepareString(arg_string, selection):
    arg_string = arg_string.split(',')[selection].strip()

    if arg_string.startswith('\'') and arg_string.endswith('\''):
        prepared_string = arg_string[1:-1]

    return prepared_string

def logOutput(output_string):
    open_file = open('IOGearLogfile.log', 'a')
    open_file.write("\n" + output_string)

    open_file.close()

def checkIOgearStatus(arglength, argcontent):
    content = str(argcontent)[1:-1]
    connections = 2
    while (connections < arglength):
        p_host = prepareString(content, connections)
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
    connections = 2
    while (connections < arglength):
        p_host = prepareString(content, connections)
        print("Attempting to connect to host: " + p_host +".....")

        try:
            tel = telnetlib.Telnet(p_host.encode('utf-8'))
        except socket.gaierror:
            print("Could not connect to " + p_host + "\nThe print server may need to be manually restarted, or the IP address verified.")
            connections += 1
            continue

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

# Main function to take input from terminal and execute functions
def selectFunction(arglength, argcontent):
    content = str(argcontent)[1:-1]
    function_select = 1

    # I want to catch the index error because it is annoying and not very helpful if a user forgets arguments
    try:
        p_string = prepareString(content, function_select)
    except IndexError:
        print("No arguments given\nUsage: function_select ip1 ip2 ip...\nAvalable functions are /reset and /check")
        sys.exit(1)

    function_string = p_string
    print("Function selected: " + function_string)
    if (function_string == "/reset" or function_string == "/r"):
        resetIOgear(arglength, argcontent)
    elif (function_string == "/check" or function_string == "/c"):
        checkIOgearStatus(arglength, argcontent)
    else:
        print ("No viable function given\nUsage: function_select ip1 ip2 ip...\nAvalable functions are /reset and /check")



# Pass command line arguments to function
selectFunction(len(sys.argv), str(sys.argv))