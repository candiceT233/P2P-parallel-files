
testPeer=$1

#dir="$testPeer"test-"$(date +%s%N | cut -b1-13)"
dir="$testPeer"test
rm -rf 2test

#waitsec=$(echo "$testPeer*2" | bc -l )
waitsec=$(($testPeer * 2))

cleanup(){
  pkill -f peer.py
  pkill -f indexserver.py
  rm -r p1/16MB*.txt
  rm -r logs/*
  sudo sync
  sudo echo "3" | sudo tee /proc/sys/vm/drop_caches
}

startp1(){
python3 peer.py << INPUTONE
1
2
16MB-1.txt
2
16MB-2.txt
2
16MB-3.txt
2
16MB-4.txt
2
16MB-5.txt
2
16MB-6.txt
2
16MB-7.txt
2
16MB-8.txt
2
16MB-9.txt
2
16MB-10.txt
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
16MB-1.txt
2
16MB-2.txt
2
16MB-3.txt
2
16MB-4.txt
2
16MB-5.txt
2
16MB-6.txt
2
16MB-7.txt
2
16MB-8.txt
2
16MB-9.txt
2
16MB-10.txt
4
INPUTONE

#sleep 5
pkill -f peer.py
pkill -f indexserver.py
pkill -f runpeer.sh
mkdir -p $dir
mv logs/* $dir
