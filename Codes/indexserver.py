import sys, os
import socket, pickle
import threading
import configparser
import time
import hashlib
import traceback
import logging
import re
import logging

CONFIG_DIR = 'configs/'
BUFFER=2048
ACK=128
peer_list ={} # key=(host,port), val={filename:filesize}
waitsec = 2

def FindPeerWithFiles(conn,addr,reqnode,reqfile):
    """TODO: done"""
    try:
        available_peers=[]
        filesize = 0
        for node in peer_list:
            # does this still work when peer_list[node] is a dictionary?
            if node != reqnode:
                if reqfile in peer_list[node]:
                    filesize = peer_list[node][reqfile] # get filesize
                    available_peers.append(node)

        msg = [filesize, available_peers]
        conn.sendall(pickle.dumps(msg))
        print(f"Available peers {available_peers}")
        print(f"Peer list given to {addr}")
        logger.info(f"Peers {available_peers} has {reqfile} given to {addr}\n")
        return
    except Exception as e:
        logger.exception('Got exception on FindPeerWithFiles')
        logger.exception(traceback.print_exc())
        #traceback.print_exc()

def ServerThreads(conn,addr):
    """TODO: done"""
    try:
        logger.info(f"Peer accept to Server: addr={addr}\n")
        print(f"Peer accept to Server: addr={addr}");

        while True:
            data = conn.recv(BUFFER)
            recvmsg = pickle.loads(data)

            if recvmsg[0] == 'REGISTER':
                peer_list[recvmsg[1]] = recvmsg[2]
                conn.sendall('REGISTERED'.encode())
                logger.info(f"Peer {addr} registered with files: {recvmsg[2]}\n")
                print(f"Peer {addr} has files: {recvmsg[2]}")

            elif recvmsg[0] == 'UPDATE':
                peer_list[recvmsg[1]] = recvmsg[2]
                logger.info(f"{addr} files updated {recvmsg[2]}\n")
                print(f"{addr} files updated {recvmsg[2]}")
            elif recvmsg[0] == 'GETFILES':
                logger.info(f"{addr} requested a list of available files\n")
                print(f"{addr} requested a list of available files")
                allfiles = set()
                for node in peer_list:
                    #print(key)
                    #print(recvmsg[1])
                    # only send files not in requested node
                    if node != recvmsg[1]:
                        for file in peer_list[node]:
                            allfiles.add(file)
                            # add only the key to list!

                conn.sendall(pickle.dumps(allfiles))

            elif recvmsg[0] == 'DOWNLOAD':
                logger.info(f"{addr} requested DOWNLOAD files: {recvmsg[2]}\n")
                print(f"{addr} requested DOWNLOAD files: {recvmsg[2]}")
                #recvmsg=[RPC,(host,port),file]
                FindPeerWithFiles(conn,addr,recvmsg[1],recvmsg[2]) # send peerlist and return

            elif recvmsg[0] == 'UNREGISTER':
                logger.info(f"Unregistering {addr}\n")
                print(f"Deleting {addr}")
                del peer_list[recvmsg[1]]
                conn.sendall('UNREGISTERED'.encode())
                break

        logger.info(f"{addr} Exited\n")
        print(f"{addr} Exited")
        conn.close()
        sys.exit()
    except Exception as e:
        #traceback.print_exc()
        #logger.exception(traceback.print_exc())
        pass

def ServerStart(server):
    try:
        server.listen()
        while True:
            conn, addr = server.accept()
            newthread = threading.Thread(target=ServerThreads, args=(conn,addr))
            newthread.start()
            print(f"Active connections: {threading.activeCount() -1}")
    except Exception as e:
        logger.exception('Got exception on ServerStart')
        logger.exception(traceback.print_exc())
        #traceback.print_exc()

def checkConfig():
    try:
        port = 60000
        host = socket.gethostbyname(socket.gethostname())
        config = configparser.RawConfigParser()
        config.add_section('Server')
        my_host = socket.gethostbyname(socket.gethostname())
        config.set('Server','host', my_host)
        config.set('Server','port',str(port))
        with open('configs/server.config', 'w') as configfile:
            config.write(configfile)

        return host, port

    except Exception as e:
        logger.exception('Got exception on checkConfig')
        logger.exception(traceback.print_exc())
        #traceback.print_exc()

def main():

    try:

        # check config files before binding
        host,port = checkConfig()
        newthread = threading.Thread(target=ServerThreads, args=(host,port))
        newthread.start()

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket object
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('',int(port))) # associate socket with host and port
        print(f"Server binded: host={host},port={port}")
        ServerStart(server)

    except Exception as e:
        logger.exception('Got exception on main')
        logger.exception(traceback.print_exc())
        #traceback.print_exc()

if __name__ == '__main__':

    logger = logging.getLogger('Example_Log')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('logs/server.log')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    logger.info("===================== Server Logging Start =====================\n")
    main()
