# P2P Parallel File Sharing System
Python socket implementation of peer to peer parallel file sharing system with an index server.

## indexserver.py
Index server will write its host and port to a configuration file under config directory named server.config. It then waits for connections with its port number. Server maintains a list of currently registered peers and their list of files in the directory as well as the size of each file.

## peer.py
The peer.py should be run after indexserver.py already started in the background. It asks for an ID in a form as a number that corresponds with the local directory. Therefore there should also be a local directory set up before running the peer. The config file will be named after the provided ID number inside config directory. For example, with id=1, the local folder should be named p1, and the config file will be named p1.config. Then the peer will register itself automatically with the server as soon as the user enters the ID. Once peer is confirmed registered, the user interface with the following options will start, as well as start its listening for other peer's connections.

### 1. Get available files list
This returns a list of files that all currently registered peers have in their local file directories. The list only contains the file name, and does not let the user know which peer node has it nor the file counts and the file sizes.

### 2. Download files from peer
The user will be prompted to input one file name only. The list is then sent to the server, and the server will send back a list of node host and port tuples and the requested file size. The peer side function will then download a chunk of file from each peer on the list. Each chunk is downloading the file on a different thread with a different socket connection. After the file is downloaded, a peer side function will update its local file names to the index server.

### 3. Delete file in my directory
The list of files in user's local directory will be displayed. The user should enter a list of exact file names seperated by space. Then the file will be deleted from the local directory and will send an updated list to the index server.

### 4. Quit
Once quit is chosen, it waist for 10 seconds then checks for other still active connecting peers and wait for their download to finishes. The peer then unregisters itself from the index server by sending a message to the index server. After index server removed the peer from its active peer list, peer will exit the program.

### 5. Sleep for 10 second (act as server only)
This choice is added and it solely would put the thread to sleep for 10 seconds. The peer will then act as a “server” that waits for file download request only. This is added to for the ease of benchmarks.

## Makefile
Make file can generate data, run test script with different inputs.

## test.sh
The script runs 2, 4, 8, and 16 active peer at the index-server then one additional peer that requests to download 10 files from all other peers. 

## runpeer.sh
The script is to start a peer and have it inactive and acting as a “server” that waits for file download requests.

