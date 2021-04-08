#!/bin/bash

if [ $# -eq 0 ]
then
	echo "bash test.sh <peer number>"
	exit 0
fi


testPeer=$1
filename="32MB"

dir="$testPeer"test-"$(date +%s%N | cut -b1-13)"
#dir="$testPeer"test

#waitsec=$(echo "$testPeer*2" | bc -l )
waitsec=$(($testPeer + 8))

cleanup(){
  pkill -f peer.py
  pkill -f indexserver.py
  rm -r p1/${filename}*.txt
  rm -r logs/*
  sudo sync
  sudo echo "3" | sudo tee /proc/sys/vm/drop_caches
}

startp1(){
python3 peer.py << INPUTONE
1
2
${filename}-1.txt
2
${filename}-2.txt
2
${filename}-3.txt
2
${filename}-4.txt
2
${filename}-5.txt
2
${filename}-6.txt
2
${filename}-7.txt
2
${filename}-8.txt
2
${filename}-9.txt
2
${filename}-10.txt
4
INPUTONE
}





# download from 8 servers
cleanup

:<<"END"
python3 indexserver.py & echo $!
until pids=$!
do
  sleep 0.01
done
END

startotherpeers(){
  for ((a=2; a<= ((${testPeer} + 1)); a++))
  do
    bash runpeer.sh $a &
  done
}

python3 indexserver.py &

startotherpeers & echo $!
until pids=$!
do
  sleep 0.1
done

sleep $waitsec
python3 peer.py << INPUTONE
1
2
${filename}-1.txt
2
${filename}-2.txt
2
${filename}-3.txt
2
${filename}-4.txt
2
${filename}-5.txt
2
${filename}-6.txt
2
${filename}-7.txt
2
${filename}-8.txt
2
${filename}-9.txt
2
${filename}-10.txt
4
INPUTONE


pkill -f peer.py
pkill -f indexserver.py
pkill -f runpeer.sh
mkdir -p $dir
mv logs/* $dir
