"""random agent that prints to a file

python3 -m pysc2.bin.agent --map CollectMineralShards --agent ungsc2.agents.obs_spy.ObsSpyAgent

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy

from ungsc2.agents import base
from pysc2.lib import actions

class ObsSpyAgent(base.BaseAgent):
	"""A random agent that prints the obs to a file"""
	def step(self, obs):
		#open the file, with w or write priviledges
		debug_file = open("/home/christian/StarCraft/ungsc2/agents/obs_debug.txt", 'w')
		#obs is a TimeStep class
		#obs.step_type
		debug_file.write('obs.step_type========\n')
		debug_file.write(str(obs.step_type))
		#obs.reward
		debug_file.write('\nobs.reward========\n')
		debug_file.write(str(obs.reward))
		#obs.discount
		debug_file.write('\nobs.discount========\n')
		debug_file.write(str(obs.discount))
		#obs.observation is a dictionary
		debug_file.write('\nobs.observation.keys========\n')
		debug_file.write(str(obs.observation.keys()))
		debug_file.write('\nobs.observation[minimap][4] or player_id========\n')
		debug_file.write(str(len(obs.observation['minimap'][4])))
		debug_file.write('\nobs.observation[single_select]========\n')
		debug_file.write(str(obs.observation['single_select']))
		debug_file.write('\nobs.observation[minimap]========\n')
		debug_file.write(str(obs.observation['minimap']))
		debug_file.write('\nobs.observation[multi_select]========\n')
		debug_file.write(str(obs.observation['multi_select']))
		debug_file.write('\nobs.observation[control_groups]========\n')
		debug_file.write(str(obs.observation['control_groups']))
		debug_file.write('\nobs.observation[build_queue]========\n')
		debug_file.write(str(obs.observation['build_queue']))
		debug_file.write('\nobs.observation[score_cumulative]========\n')
		debug_file.write(str(obs.observation['score_cumulative']))
		debug_file.write('\nobs.observation[cargo_slots_available]========\n')
		debug_file.write(str(obs.observation['cargo_slots_available']))
		debug_file.write('\nobs.observation[screen]========\n')
		debug_file.write(str(obs.observation['screen']))
		debug_file.write('\nobs.observation[game_loop]========\n')
		debug_file.write(str(obs.observation['game_loop']))
		debug_file.write('\nobs.observation[cargo]========\n')
		debug_file.write(str(obs.observation['cargo']))
		debug_file.write('\nobs.observation[available_actions]========\n')
		debug_file.write(str(obs.observation['available_actions']))
		debug_file.write('\nobs.observation[player]========\n')
		debug_file.write(str(obs.observation['player']))


		#this is the RandomAgent code
		super(ObsSpyAgent, self).step(obs)
		function_id = numpy.random.choice(obs.observation["available_actions"])
		args = [[numpy.random.randint(0, size) for size in arg.sizes]
			for arg in self.action_spec.functions[function_id].args]
		return actions.FunctionCall(function_id, args)
