import socket
import os
import threading
import socket, pickle
import configparser
import random
import hashlib
import logging
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import multiprocessing
import traceback
import math

# META: a unique ID?
# META: a list of files hosted by me
myFiles=[]
myEntry=[]
# META: my file directory
# META: list of connected peers
CONFIG_DIR = 'configs/'
BUFFER=4096
ACK=128
CHUNKSIZE = 2097152 # 2MB
downloadtime=[]
sendtime=[]
myFiles = {}

MENU= """================= MENU =================
1. Get available files list
2. Download files from peer
3. Delete file in my directory
4. Quit
5. Sleep for 10 second (act as server only)
========================================\n"""

#targetpeer[id], file, filesize, filecontent
def downloadThread(peer, filename, filesize, chunkID, filecontent):
    try:
        c_host, c_port = peer

        newc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        newc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # ['DOWNLOAD',filename, CHUNKSIZE, chunkID]
        newc.connect((c_host, int(c_port)))
        message = ['DOWNLOAD', filename, CHUNKSIZE, chunkID]
        newc.sendall(pickle.dumps(message))

        data = []

        while True:
            newc.settimeout(5)
            packet = newc.recv(BUFFER)
            if not packet: break
            data.append(packet)
        content = pickle.loads(b"".join(data))

        # content = [chunkID, hashcode, filecontent]
        recvID = content[0]

        if recvID == 0:
            recvHash =content[1]
            filecontent.update({recvID:[recvHash, content[2]]})
        else:
            filecontent.update({recvID:content[1]})

        #logger.info(f"received content= {filecontent}")

    except:
        logger.exception('Got exception on downloadThread')
        logger.error(f"Error: c_host={c_host} c_port={c_port}")
        logger.exception(traceback.print_exc())


def donwload(p_client,my_dir,my_host,s_port):
    try:

        #myFiles = os.listdir(my_dir);
        file=input("Enter one file name you want to download:")

        message = ['DOWNLOAD',(my_host,s_port),file]
        p_client.sendall(pickle.dumps(message))
        data = p_client.recv(BUFFER) # [filesize, [available_peers]]
        msg = pickle.loads(data)

        """
        count=0
        while not msg and count <5:
            try:
                data = p_client.recv(BUFFER)
                msg = pickle.loads(data)
                if msg: break
            except socket.error:
                print("Fail to connect, retry after 0.5 second")
                count+=1
                time.sleep(0.5)
        """

        if not msg:
            return 'No peers'

        filesize = msg[0]
        peerlist = msg[1]
        numpeer = len(peerlist)
        targetpeer = []
        threads=[]

        #print("filesize=",filesize)
        chunknum = math.ceil(filesize/CHUNKSIZE)
        chunkid = list(range(chunknum))

        #print("chunkid=",chunkid)

        for id in chunkid:
            index = id%numpeer
            targetpeer.append(peerlist[index])

        filecontent = {}

        dl_st = time.time()
        if peerlist:
            for id in chunkid:

                newthread = threading.Thread(target=downloadThread,
                args=(targetpeer[id], file, filesize, id, filecontent))
                newthread.start()
                threads.append(newthread)

        for t in threads:
            t.join()

        recv_hash = 0

        f=open(f'{my_dir}/{file}','w')

        for id in chunkid:
            if id == 0:
                recv_hash=filecontent[id][0]
                f.write(filecontent[id][1])
            else:
                f.write(filecontent[id])

        f.close()

        f=open(f'{my_dir}/{file}','r')

        my_hash = hashlib.md5(f.read().encode())
        my_hash = my_hash.digest() # in byte format
        f.close()
        #logger.info(f"myhash={my_hash}\nrecvHash={recv_hash}")

        if recv_hash == my_hash: # compare hash
            # store file to local directory
            logger.info(f"File downloaded: {file}\n")
            downloadtime.append(time.time()-dl_st)
            print(f"File downloaded: {file}")

        else:
            logger.error(f"Download Failed: {file}\n")
            print(f"Download Failed: {file}")

        return 'FINISHED'
        # Handle peer closing connection?
    except Exception as e:
        logger.exception('Got exception on delete')
        logger.exception(traceback.print_exc())



def delete(my_dir):
    try:
        #myFiles = os.listdir(my_dir)
        removed=[]
        print(f"Your current files: {myFiles}")
        files=input("File name(s) you want to delete seperated by space:")
        files = list(files.split(" "))

        for file in files:
            if file in myFiles:
                os.remove(f'{my_dir}/{file}')
                del myFiles[file]
            else:
                print(f"{file} not in your direcotry")
                logger.error(f"{file} not in your direcotry")

        logger.info(f"You removed {removed} from your direcotry.\n")
        print(f"You removed {removed} from your direcotry.")

        return myFiles

    except Exception as e:
        logger.exception('Got exception on delete')
        logger.exception(traceback.print_exc())

# listen on other peer's connection
def MyServerThread(conn, addr, my_dir):

    try:

        logger.info(f"Peer connect: addr={addr}\n")
        print(f"Peer connect: addr={addr}");

        data = conn.recv(BUFFER)
        recvmsg = pickle.loads(data)

        #['DOWNLOAD',filename, CHUNKSIZE, chunkID]
        file = recvmsg[1]
        csize= recvmsg[2]
        chunkID = recvmsg[3]
        offset = csize*chunkID
        packet=[]
        send_st = time.time()

        if recvmsg[0] == 'DOWNLOAD':
            if os.path.exists(my_dir+"/"+file):
                f=open(my_dir+"/"+file,'r')
                # https://www.geeksforgeeks.org/md5-hash-python/
                filehash=hashlib.md5(f.read().encode())
                filehash = filehash.digest()
                f.seek(offset,0)
                content = f.read(csize)
                # packet
                # content = [chunkID, hashcode, filecontent]
                packet.append(chunkID)
                if chunkID == 0:
                    packet.append(filehash)
                packet.append(content)
                #logger.info(f"packet={packet}\n\n")
                #packet[chunkID, filehash, content]
                conn.sendall(pickle.dumps(packet))
                sendtime.append(time.time() - send_st)
                logger.info(f"{file} send to {addr}: chunk number= {chunkID} time={time.time()}\n")
                print(f"{file} send to {addr}: chunk number= {chunkID} time={time.time()}\n")
                f.close()
            else:
                logger.info(f"File does not exist: {file}")
                print(f"File does not exist: {file}")

        conn.close()
        print(f"{addr} download completed.")
        logger.info(f"{addr} download completed.\n")
        logger.info(f"Requested download {len(sendtime)} times\n")
        logger.info(f"Average response time: {sum(sendtime)/len(sendtime)}\n")
        return

    except Exception as e:
        logger.exception('Got exception on MyServerThread')
        logger.exception(traceback.print_exc())


def MyServerStart(my_host, s_port, my_dir):
    try:
        # server socket object
        p_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        p_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        p_server.bind(('',int(s_port))) # associate socket with host and port
        logger.info(f"Your peer is binded: host={my_host}, port={s_port}\n")
        print(f"Your peer is binded: host={my_host}, port={s_port}")

        p_server.listen() # default 5 backlog
        print(f"Your peer is listening on {my_host}...")
        serverthreads=[]
        while True:

            conn, addr = p_server.accept()
            with ThreadPoolExecutor(max_workers=os.cpu_count()+10) as executor:
                future = executor.submit(MyServerThread, conn, addr, my_dir)

        p_server.close()
    except Exception as e:
        logger.exception('Got exception on MyServerStart')
        logger.exception(traceback.print_exc())

# client related operations
def MyClientStart(p_client, my_host, s_port, myID):
    try:
        # register with server
        # give server my local list
        print(f"Server accepted p{myID}...")
        my_dir = f"p{myID}/"
        files = os.listdir(my_dir);
        for file in files:
            fsize = os.path.getsize(f'{my_dir}{file}')
            myFiles[file] = fsize

        #print("myFiles before register=",myFiles)
        myEntry = ['REGISTER',(my_host,s_port), myFiles]
        p_client.sendall(pickle.dumps(myEntry));
        print(f"Registering my file list to index server...")
        ack = p_client.recv(ACK);

        if ack.decode() == 'REGISTERED':
            print("You are now registered at server.")
            logger.info("You are now registered at server.\n")

            s_thread = threading.Thread(target=MyServerStart,
            args=(my_host,s_port,my_dir))
            s_thread.start()

            while True:

                print(MENU);
                choice = input("Please choose an operation:")
                # run user method to download files
                if choice == '1':
                    logger.info("Requested a list of files from other peers.\n")
                    message = ['GETFILES',(my_host,s_port)]

                    p_client.sendall(pickle.dumps(message))
                    data = p_client.recv(BUFFER)

                    counter=0
                    while not data and counter < 5:
                        logger.info("No other peer, request again in 0.5 sec\n")
                        time.sleep(0.5)
                        with lock:
                            message = ['GETFILES',(my_host,s_port)]
                            p_client.sendall(pickle.dumps(message))
                            data = p_client.recv(BUFFER)
                            counter+=1

                    if data:
                        allfiles = pickle.loads(data)
                        print(f"Files available at all other peers:{allfiles}")
                        logger.info(f"Files available at other peers:{allfiles}\n")
                    else:
                        print(f"Currently no other peer on server.")

                elif choice == '2': #Download file\n
                    if donwload(p_client,my_dir,my_host,s_port) != 'FINISHED':
                        # update my file list
                        print("Please retry download.")
                    else:

                        files = os.listdir(my_dir);
                        for file in files:
                            fsize = os.path.getsize(f'{my_dir}{file}')
                            myFiles[file] = fsize

                        message = ['UPDATE',(my_host,s_port),myFiles]
                        p_client.sendall(pickle.dumps(message));

                elif choice == '3': # delete files in my directory
                    delete(my_dir)
                    # update list to index server
                    message = ['UPDATE',(my_host,s_port),myFiles]
                    p_client.sendall(pickle.dumps(message));
                elif choice == '5':
                    time.sleep(10)

                elif choice == '4': #quit
                    counter = 0
                    while threading.activeCount() >2:
                        logger.info(f"Current thread counts: {threading.activeCount()}\n")
                        counter +=1
                        time.sleep(0.5)

                    msg = ['UNREGISTER',(my_host,s_port)]
                    p_client.sendall(pickle.dumps(msg))
                    ack = p_client.recv(ACK);
                    logger.info(f"p{myID} unregistering from server")

                    if len(downloadtime):
                        logger.info(f"Downloaded from peer {len(downloadtime)} times\n")
                        logger.info(f"Average download time {sum(downloadtime)/len(downloadtime)}\n")

                    if len(sendtime):
                        logger.info(f"Requested download {len(sendtime)} times\n")
                        logger.info(f"Average response time: {sum(sendtime)/len(sendtime)}\n")

                    if ack.decode() == 'UNREGISTERED':
                        print("Exiting...")
                        logger.info(f"p{myID} unregistered and exiting...")
                        p_client.close()
                        os._exit(1)
                        break
                    else:
                        print(f"Current thread counts: {threading.activeCount()}")
                else:
                    print("Please enter valid option.")
        else:
            print("Fail to register at server, please retry")
        return 'NOTREGISTER'
    except Exception as e:
        logger.exception('Got exception on MyClientStart')
        logger.exception(traceback.print_exc())

def set_my_config(myID,is_host, is_port):
    try:
        config = configparser.RawConfigParser()
        config.add_section('Peer')
        my_host = socket.gethostbyname(socket.gethostname())
        config.set('Peer','serverhost',is_host)
        config.set('Peer','serverport',is_port)
        my_port = int(is_port) + int(myID)
        config.set('Peer','myhost', my_host)
        config.set('Peer','myPort',my_port)
        config.set('Peer','mydir',f"p{myID}/")
        with open(f'configs/p{myID}.config', 'w') as configfile:
            config.write(configfile)

        return my_host, my_port
    except Exception as e:
        logger.exception('Got exception on set_my_config')
        logger.exception(traceback.print_exc())


def get_server_config():
    config = configparser.ConfigParser()
    config.read(f'configs/server.config')
    is_port= int(config['Server']['port'])
    is_host=config['Server']['host']
    return is_host, is_port


# connects to server and listens to other peers
def main(myID):
    try:
        is_host, is_port = get_server_config() # index server info
        # setup config
        my_host, my_port = set_my_config(myID, is_host, is_port)

        # client socket object
        p_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        p_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("Connecting server...")
        p_client.connect((is_host,is_port))
        status = MyClientStart(p_client, my_host, my_port, myID)
        # Handle 'NOTREGISTER'

    except Exception as e:
        logger.exception('Got exception on main()')
        logger.exception(traceback.print_exc())

if __name__ == '__main__':
    # set up IP and Port
    try:
        con = True
        while con:

            myID=input("Please enter your file directory id (a number greater than 0):")

            if not os.path.exists(f'p{myID}'):
                print(f"No direcotry p{myID} exist")
                print("Continue with a new empty direcotry?")

                choice=input("[c-continue/e-exit]:")
                if(choice == 'c'):
                    os.mkdir(f"./p{myID}")
                    con = False
                else:
                    print('Exiting...')
                    exit(1)
            else:
                con = False

        logger = logging.getLogger("Example_Log")
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(f"logs/p{myID}.log")
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        logger.info(f"===================== Peer {myID} Logging Start =====================")

        main(myID)

    except Exception as e:
        logger.exception('Got exception on main')
        logger.exception(traceback.print_exc())
