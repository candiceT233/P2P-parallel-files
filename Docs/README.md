# P2P File Sharing System
Python socket implementation of peer to peer file sharing system with a index server.

## indexserver.py
Index server will write its host and port to a configuration file under config directory named server.config. It then waits for connections with its port number. Server maintains a list of currently registered peers and a list of file names each peer has in theri local directories.


## peer.py
The peer.py should be run after indexserver.py already started in tthe background. It asks for a ID in a form as a number that corresponds with the local file name to generate a config file. For example, with id=1, the local folder should be named p1, and the config file will be named p1.config. Then the peer will starts to register itself with the server as soon as user entered the ID. Once peer is confirmed registered, the user interface with the following options will starts, as well as starts its listening for other peer's connection.

### 1. Get available files list
This return a list of files that all currently registered peers have in their local file directories. The list only contain the file name, does not let the user know which peer node has it or how many files with the same name.

### 2. Download files from peer
The user will be prompted to input file name exactly as it is seperated by space. The list is then send to the server, and the server will send back a list of node host and port tuples. The peer side function will then randomly choose a peer to connect to and starts downloading the file. After file is downloaded, a peer side function will update its local file names to the index server.

### 3. Delete file in my directory
The list of files in user's local directory will be displayed. The user should enter a list of exact file names seperated by space. Then the file will be deleted from the local directory and will send an updated list to the index server.

### 4. Quit
Once quit is chosen, it waist for 10 seconds then checks for other still active connecting peers and wait for their download to finishes. The peer then unregisters itself from the index server by sending a message to the index server. After index server removed the peer from its active peer list, peer will exit the program.


## Makefile
Make file runs query response time tests and file transfer time tests. Then it organizes all the test output log files into a folder named test-logs.

## response-time.sh
The script runs 2, 4, and 8 concurrent peers to test for index-server response time. Each peer will request to download one file, with a total of 60 requests. The averaged recorded time is recorded in the regular peer log file.

## transfer-time.sh
The script tests for 4 concurrent peers requesting to download 5 files of different sizes. The sizes are 128 bytes, 512 bytes, 2kb, 8kb, and 32kb.

## filegenerator.py
Enter the file directory (or a list of file directories seperated by space), the file size in bytes (or a list of file sizes seperated by space), then the number of files each file size you want, then the choice of adding the file directory as the file name prefix. Then it generates the files with random ASCII strings.
