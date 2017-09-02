#this is exploratory analysis of .SC2Replay files
#python3 ~/StarCraft/cwatts/replay_ripper/read_replay.py

from os import walk
import random

replays = []

#this will go into the directories and make a list of files and folders
#for each deeper directory it goes into
#I only care about the first one so I break after one run 
path = '/home/christian/StarCraftII/Replays/'
for (dirpath, dirnames, filenames) in walk(path):
	replays.extend(filenames)
	break

#there are a lot of replays here
print(len(replays))

#get one at random
r = path + replays[random.randrange(0,len(replays))]
print(r)


