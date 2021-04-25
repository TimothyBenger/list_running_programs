Usage:

1) Save the server.py script on the server machine, make it executable
2) Set the HOST parameter on line 14 of list_client_programs.py to the ip address of the server
2) Save the list_client_programs.py script on the client machine, make it executable
3) Run ./server.py on the server machine
4) Run ./list_client_programs.py on the client machine
5) Running program data will be saved to the same repository as the script

Notes / Improvements:

* Only supports IPv4
* Should be capturing any errors opening/closing files/sockets
* Should consider rotation/cleanup of output files
* Size of data sent / read - is 1024 optimal?
* Clearer usage information and addition of --help output
* Messy to use temporary file for processing data on client side
* Also slow, would be better to use in-memory buffer
* Also the temp file never gets cleaned up
* No failure tolerance, if the script breaks, no more data until we run list_client_programs and server again
* Would be better to leave server open and run client process as a cronjob
* Needs linting
* Should abstract repeated code - (e.g. logic to create the unique filenames)
* Not much logging output for user
* No requirements.txt or package structure (though no requirements beyond python3)
* Question mark over portability to other operating systems
* Re the "EOF" marker, server.py should deal with normal case first, exceptional case after
* What if a process has the string "EOF" in its name?
* 5 seconds is a magic value, should be at least a constant, better a command line option
* Server IP address is a magic value, should be a command line option


Tests to consider:

* Test that all of mock ps output data turns up in output file as expected (i.e. output file is complete)
* Test output file contains no duplicate information
* Test output file contains no information that is not in mock ps output data (i.e. output file is accurate)
* Test what would happen if process interrupted on either machine (currently would fail)