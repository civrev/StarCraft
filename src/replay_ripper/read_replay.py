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
from pysc2.lib import features
from pysc2.lib import point
from s2clientprotocol import sc2api_pb2 as sc_pb


size = point.Point(16, 16)
interface = sc_pb.InterfaceOptions(raw=True, score=False,
	feature_layer=sc_pb.SpatialCameraSetup(width=24))
size.assign_to(interface.feature_layer.resolution)
size.assign_to(interface.feature_layer.minimap_resolution)


#this is the code from pysc2, modified for my purposes

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
		info = controller.replay_info(replay_data_x(replay_path))
		print("-" * 60)
		map_name = info.map_name
		map_name = map_name.replace(" ", "") + ".SC2Map"
		print("MAP NAME: " + map_name)
		print("-" * 60)
		print(info)
		print("-" * 60)
		
		#now that I have the summary info, I can pass to process replay
		#I want everything for player 1 and 2
		for player_id in [1,2]:
			replay_data = replay_data_x(replay_path)
			map_data = run_config.map_data(map_name)
			process_replay(controller,replay_data,map_data,player_id)
		 

#this was taken from run_config
def replay_data_x(replay_path):
	"""Return the replay data given a path to the replay."""
	#'rb' is what makes this work
	#which is not the same as normal open() arg 'r+b'
	#this goes beyond binary decoding
	with gfile.Open(replay_path, 'rb') as f:
		return f.read()

#this was taken from replay_actions.py and modified it
def process_replay(controller, replay_data, map_data, player_id):
	"""Process a single replay, updating the stats."""
	print("start_replay")

	#this is where is actually starts the game engine to process the replays
	controller.start_replay(sc_pb.RequestStartReplay(
		replay_data=replay_data,
		map_data=map_data,
		options=interface,
		observed_player_id=player_id))

	feat = features.Features(controller.game_info())

	print("step")
	controller.step()
	while True:
		print("observe")
		obs = controller.observe()


		for action in obs.actions:
			act_fl = action.action_feature_layer
			if act_fl.HasField("unit_command"):
				print(act_fl.unit_command.ability_id)
			if act_fl.HasField("camera_move"):
				print('camera_move')
			if act_fl.HasField("unit_selection_point"):
				print('unit_selection_point')
			if act_fl.HasField("unit_selection_rect"):
				print('unit_selection_point')
			if action.action_ui.HasField("control_group"):
				print('control_group')

			try:
				func = feat.reverse_action(action).function
			except ValueError:
				func = -1
			print(func)

		for valid in obs.observation.abilities:
			print(valid.ability_id)

		for u in obs.observation.raw_data.units:
			print(u.unit_type)

		for ability_id in feat.available_actions(obs.observation):
			print(ability_id)

		if obs.player_result:
			break

		print("step")
		#gflags is not working per se, so I tried this
		step_mul = 8
		controller.step(step_mul)


def main():  # Needed so the setup.py scripts work.
	app.really_start(_main)


if __name__ == "__main__":
	main()
