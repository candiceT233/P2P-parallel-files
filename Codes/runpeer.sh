

#echo "PeerID=$peerID time: $(date +"%T" )" # current time
peerID=$1


python3 peer.py << INPUTONE
${peerID}
5
5
5
5
5
5
5
5
5
5
4
INPUTONE
