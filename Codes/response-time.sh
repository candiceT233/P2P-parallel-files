rm -f logs/*.log
#logfile=transfer-speed.log
#echo -n "" > $logfile


setupenv(){
  kill -f peer.py
  kill -f peer.py
  # cleanup data sets
  for i in {1..8}
  do
    rm -rf p$i
  done

# set up test datas
python3 filegenerator.py <<RAW_INPUT
p1 p2 p3 p4 p5 p6 p7 p8
128 512 2048 8192 32768
10
n
RAW_INPUT
}


# start server
pkill -f indexserver.py
pkill -f indexserver.py
wait
python3 indexserver.py &
echo "Server started"

sleep 1

setupenv
echo"**********test 2 threads**********"
bash runpeer.sh 1 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 2

sleep 2
pkill -f peer.py
pkill -f runpeer.sh
rm -rf 2trun
mkdir 2trun
mv logs/p*.log 2trun


echo"**********test 4 threads**********"
bash runpeer.sh 1 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 2 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 3 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 4


sleep 4
pkill -f peer.py
pkill -f runpeer.sh
rm -rf 4trun
mkdir 4trun
mv logs/p*.log 4trun

# round 1 of 8 nodes
bash runpeer.sh 1 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 2 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 3 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 4 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 5 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 6 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 7 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 8

sleep 5
pkill -f peer.py
pkill -f runpeer.sh
rm -rf 8trun-1
mkdir 8trun-1
mv logs/p*.log 8trun-1


# round 1 of 8 nodes
bash runpeer.sh 1 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 2 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 3 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 4 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 5 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 6 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 7 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 8

sleep 5
pkill -f peer.py
pkill -f runpeer.sh
rm -rf 8trun-2
mkdir 8trun-2
mv logs/p*.log 8trun-2


# round 3 of 8 nodes
bash runpeer.sh 1 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 2 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 3 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 4 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 5 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 6 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 7 & echo $!
until pids=$!
do
  sleep 0.0001
done
bash runpeer.sh 8

sleep 5
pkill -f peer.py
pkill -f runpeer.sh
rm -rf 8trun-3
mkdir 8trun-3
mv logs/p*.log 8trun-3

pkill -f indexserver.py
# cleanup data sets
for i in {1..8}
do
  rm -rf p$i
done


trap "killall background" EXIT
