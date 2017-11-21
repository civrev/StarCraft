#!/bin/bash
echo "Ran using $chmod +x train.sh"
echo "Preparing training data 1/5"
python3 -m pysc2.bin.agent --map CollectMineralShards --agent ungsc2.agents.scripted.CollectMineralShards
echo "Preparing training data 2/5"
python3 -m pysc2.bin.agent --map CollectMineralShards --agent ungsc2.agents.scripted.CollectMineralShards
echo "Preparing training data 3/5"
python3 -m pysc2.bin.agent --map CollectMineralShards --agent ungsc2.agents.scripted.CollectMineralShards
echo "Preparing training data 4/5"
python3 -m pysc2.bin.agent --map CollectMineralShards --agent ungsc2.agents.scripted.CollectMineralShards
echo "Preparing training data 5/5"
python3 -m pysc2.bin.agent --map CollectMineralShards --agent ungsc2.agents.scripted.CollectMineralShards

