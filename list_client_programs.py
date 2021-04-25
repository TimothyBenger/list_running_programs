#!/usr/bin/env python3

# usage: ./list_client_programs
# run on the client machine, after first having run
# ./server.py on the server machine

# Every 5 seconds, list_client_programs lists running programs on the machine
# where the script is run, and writes to the endpoint specified in HOST/PORT

import socket
import subprocess
import time

HOST = '87.254.4.136'  # server's  IP address
PORT = 65500           # port used by server
TEMP_FILE = "/tmp/running_programs.txt"

# instantiate a TCP socket (ipv4)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    # connect to the server
    s.connect((HOST, PORT)) 
    
    # open a temporary file for the ps subprocess call to use as stdout
    f = open(TEMP_FILE, "w+")
    
    while True:
        # use ps to get currently executing programs for all users
        subprocess.call(["ps", "aux"], stdout=f)

        # ensure cursor is at start of tempfile, read 1024 bytes of ps output
        f.seek(0)
        ps_data = f.read(1024)

        # until we reach EOF:
        #   send the encoded output
        #   read another 1024 bytes of data
        while ps_data:        
            s.send(ps_data.encode("utf-8"))
            ps_data = f.read(1024)

        # clear the file for future use
        f.seek(0)
        f.truncate()

        # send the EOF marker that server uses to differentiate
        # between outputs of ps run at two different times  that show up in
        # same 1024-byte chunk
        s.send("EOF".encode("utf-8"))

        # only want to run every 5 seconds
        time.sleep(5)