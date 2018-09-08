#!/bin/bash

ph=$1
./encodeGambler.sh $ph > ./tmp/mdp_gambler_${ph}.txt
echo 'solving..'
./planner.sh --algorithm hpi --mdp tmp/mdp_gambler_${ph}.txt > tmp/policy_gambler_${ph}.txt
echo 'done.'
python3 extras/plot_gambler.py -f tmp/policy_gambler_${ph}.txt