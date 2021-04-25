#!/usr/bin/env python3

# usage: ./server.py
# run on the server machine, before running ./list_client_programs on the
# client machine

# listen for data about running programs on the client (ps aux)
# write this data to timestamped files, each containing one ps aux output

import socket
import time

HOST = ''           # server will accept all any availableipv4 connections
PORT = 65500        # port to listen on

# instantiate a TCP socket (ipv4)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    # bind to 65500, start listening and block waiting on new connections
    # when a client connects, return:
    #   conn   --->  socket object
    #   addr   --->  tuple holding the (host, port) of the client
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept() # block and wait for new connections

    # hold the connection open
    with conn:
        print('Connected by', addr)

        # create a unique file for the ps output at current time
        time_now = str(time.time()).replace(".","-")
        fname = f"running_programs_{time_now}.txt"

        # open for appending
        f = open(fname, 'a')

        while True:

            # read whatever data the client sends
            data = conn.recv(1024)
            if not data:
                break
            
            # decode bytestream, we want readable output
            text_data = data.decode("utf-8")
            
            # the 1024 byte chunk may include the end of one ps output and the
            # start of another, in which case it will be divided with an "EOF"
            # marker. Where this is the case, split that data and write to the
            # end/start of the current/next file as appropriate
            if "EOF" in text_data:
                
                end_previous, start_next = text_data.split("EOF")
                f.write(end_previous)
                # finished with this file, close it
                f.close()

                # and create a new unique file for the next ps output
                time_now = str(time.time()).replace(".","-")
                fname = f"running_programs_{time_now}.txt"
                f = open(fname, 'a')
                f.write(start_next)
            
            # normal case, a 1024-byte chunk of ps data
            else:
                print("no EOF in data, write to file as normal")
                f.write(text_data)
