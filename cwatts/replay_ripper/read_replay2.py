#reading .SC2Replay files
#python3 -m cwatts.replay_ripper.read_replay2

import random
import os
import struct

replays_x = []
path = '/home/christian/StarCraftII/Replays/'
for (dirpath, dirnames, filenames) in os.walk(path):
	replays_x.extend(filenames)
	break
path = path + replays_x[random.randrange(0,len(replays_x))]

with open(path, 'r+b') as file:
	contents = file.read()
	print(struct.unpack("iiiii", contents[:20]))
	print(struct.unpack("i" * ((len(contents) -24) // 4), contents[20:-4]))
	struct.unpack("i", contents[-4:])
