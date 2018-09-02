#!/bin/bash

PWD=`pwd`


base_port=5001
hostname="localhost"

# Allowed values for algorithm parameter(case-sensitive)
# 1. epsilon-greedy
# 2. UCB
# 3. KL-UCB
# 4. Thompson-Sampling
# 5. rr

numArms=$1
instance_file=$2
horizon=$3
algorithm=$4
epsilon=$5

start=$6
end=$7
num_runs=$((end - start))

MAIN_LOG_DIR="${PWD}/logs/${instance_file}_${horizon}"
mkdir -p "${MAIN_LOG_DIR}"

if [ "$algorithm" == "epsilon-greedy" ]; then
    LOG_DIR="${MAIN_LOG_DIR}/${algorithm}_${epsilon}"
else
    LOG_DIR="${MAIN_LOG_DIR}/${algorithm}"
fi

mkdir -p "${LOG_DIR}"

DATA_DIR="${PWD}/data"
SERVERDIR="${PWD}/server"
CLIENTDIR="${PWD}/client"

banditFile="${DATA_DIR}/${instance_file}.txt"
echo $LOG_DIR
for ((i=${start}; i<${end}; i++));
do
    port=$((base_port + i))
    OUTPUTFILE="${LOG_DIR}/serverlog_$i.txt"
    randomSeed=$i
    printf "\r $i/${num_runs}"
    # echo "$i, port:${port}"
    pushd $SERVERDIR > /dev/null
    # echo "starting server.."
    cmd="./startserver.sh $numArms $horizon $port $banditFile $randomSeed $OUTPUTFILE"
    # echo $cmd
    $cmd
    popd > /dev/null

    # sleep 1

    pushd $CLIENTDIR > /dev/null
    cmd="./startclient.sh $numArms $horizon $hostname $port $randomSeed $algorithm $epsilon"
    #echo $cmd
    $cmd
    popd > /dev/null
done;
echo ""
