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

	path = path + replays_x[random.randrange(0,len(replays_x))]

	try:
		if gfile.IsDirectory(path):
			return _replay_index(path)
		else:
			return _replay_info(path)
	except KeyboardInterrupt:
		pass


def _replay_index(replay_dir):
	"""Output information for a directory of replays."""
	run_config = run_configs.get()
	replay_dir = run_config.abs_replay_path(replay_dir)
	print("Checking: ", replay_dir)

	with run_config.start() as controller:
		print("-" * 60)
		print(",".join((
			"filename",
			"build",
			"map_name",
			"game_duration_loops",
			"players",
			"P1-outcome",
			"P1-race",
			"P1-apm",
			"P2-race",
			"P2-apm",
		)))

		bad_replays = []
		for file_path in run_config.replay_paths(replay_dir):
			file_name = os.path.basename(file_path)
			info = controller.replay_info(run_config.replay_data(file_path))
			if info.HasField("error"):
				print("failed:", file_name, info.error, info.error_details)
				bad_replays.append(file_name)
			else:
				out = [
					file_name,
					info.base_build,
					info.map_name,
					info.game_duration_loops,
					len(info.player_info),
					sc_pb.Result.Name(info.player_info[0].player_result.result),
					sc_pb.Race.Name(info.player_info[0].player_info.race_actual),
					info.player_info[0].player_apm,
				]
				if len(info.player_info) >= 2:
					out += [
					sc_pb.Race.Name(info.player_info[1].player_info.race_actual),
					info.player_info[1].player_apm,
					]
				print(u",".join(unicode(s) for s in out))
			if bad_replays:
				print("Replays with errors:")
				print("\n".join(bad_replays))


def _replay_info(replay_path):
	"""Query a replay for information."""
	if not replay_path.lower().endswith("sc2replay"):
		print("Must be a replay.")
		return

	run_config = run_configs.get()
	with run_config.start() as controller:
		info = controller.replay_info(run_config.replay_data(replay_path))
	print("-" * 60)
	print(info)

def main():  # Needed so the setup.py scripts work.
	app.really_start(_main)


if __name__ == "__main__":
	main()
