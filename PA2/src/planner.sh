#!/bin/sh

MDP_PATH="<absolute_path>"
MDP_ALGORITHM="<lp/hpi>"

function usage()
{
    echo "mdp planner"
    echo ""
    echo "./planner.sh"
    echo "\t-h --help"
    echo "\t--mdp $MDP_PATH"
    echo "\t--algorithm $MDP_ALGORITHM"
    echo ""
}

while [ "$1" != "" ]; do
    PARAM=$1
    VALUE=$2
    case $PARAM in
        -h | --help)
            usage
            exit
            ;;
        --mdp)
            MDP_PATH=$VALUE
            ;;
        --algorithm)
            MDP_ALGORITHM=$VALUE
            ;;
        *)
            echo "ERROR: unknown parameter \"$PARAM\""
            usage
            exit 1
            ;;
    esac
    shift
    shift
done

python3 extras/mdp.py --mdp $MDP_PATH --algorithm $MDP_ALGORITHM