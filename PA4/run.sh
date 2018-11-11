#!/bin/bash

env=$1
logdir=$2
alpha=$3
epsilon=$4
num_episodes=$5
num_runs=$6

for i in $(seq 1 $num_runs);
do
    echo "random seed = $i ..."
    python3 sarsa.py --env $env --logdir $logdir --alpha $alpha\
     --gamma 1 --epsilon $epsilon --episodes $num_episodes --seed $i
    echo ""
done

python3 plot.py --logdir $logdir