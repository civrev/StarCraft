"""random agent that prints to a file"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy

from cwatts.agents import base
from pysc2.lib import actions

class ObsSpyAgent(base.BaseAgent):
	"""A random agent that prints the obs to a file"""
	def step(self, obs):
		#open the file, with w or write priviledges
		debug_file = open("/home/christian/StarCraft/cwatts/agents/obs_debug.txt", 'w')
		debug_file.write('New Obs @')
		debug_file.write(str(obs))

		#this is the RandomAgent code
		super(ObsSpyAgent, self).step(obs)
		function_id = numpy.random.choice(obs.observation["available_actions"])
		args = [[numpy.random.randint(0, size) for size in arg.sizes]
			for arg in self.action_spec.functions[function_id].args]
		return actions.FunctionCall(function_id, args)
