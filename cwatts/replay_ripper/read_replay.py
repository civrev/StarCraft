#this is exploratory analysis of .SC2Replay files
#python3 -m cwatts.replay_ripper.read_replay

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import random

from pysc2 import run_configs

from pysc2.lib import app
from pysc2.lib import gfile
from s2clientprotocol import sc2api_pb2 as sc_pb

#this is the code from replay_info.py, modified for my purposes

#you run this module without arguments
def _main(argv=()):
	replays_x = []
	path = '/home/christian/StarCraftII/Replays/'

	#this will go into the directories and make a list of files and folders
	#for each deeper directory it goes into
	#I only care about the first one so I break after one run 
	for (dirpath, dirnames, filenames) in os.walk(path):
		replays_x.extend(filenames)
		break

	#it will pull a replay at random
	path = path + replays_x[random.randrange(0,len(replays_x))]

	try:
			return _replay_info(path)
	except KeyboardInterrupt:
		pass

#this is the function where replay info is opened
def _replay_info(replay_path):
	"""Query a replay for information."""
	if not replay_path.lower().endswith("sc2replay"):
		print("Must be a replay.")
		return
	
	run_config = run_configs.get()
	print("-" * 60)
	print("\n"+str(type(run_config))+'\n')
	print('\n'+str(type(run_config.start()))+'\n')

	#this is ultimately how the replay gets read, this tiny part
	run_config = run_configs.get()
	with run_config.start() as controller:
		info = controller.replay_info(replay_data(replay_path))
	print("-" * 60)
	print(info)

#this was taken from run_config
def replay_data(replay_path):
	"""Return the replay data given a path to the replay."""
	#'rb' is what makes this work
	#which is not the same as normal open() arg 'r+b'
	#this goes beyond binary decoding
	with gfile.Open(replay_path, 'rb') as f:
		return f.read()


def main():  # Needed so the setup.py scripts work.
	app.really_start(_main)


if __name__ == "__main__":
	main()
