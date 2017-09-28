"""
A learning agent for starcraft, with comments!


python3 -m pysc2.bin.agent --map CollectMineralShards --agent ungsc2.agents.crystal_learner.CrystalLearnerAgent
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

from pysc2.lib import actions

class CrystalLearnerAgent(object):
	"""Learning agent for solving crystal shards"""
	def __init__(self):
		self.episodes = 0
		self.obs_spec = None
		self.action_spec = None
		self.old_act = -1
		self.actions = [Action(0),
				Action(1),
				Action(2),
				Action(3),
				Action(4),
				Action(7)]

	def setup(self, obs_spec, action_spec):
		self.obs_spec = obs_spec
		self.action_spec = action_spec

	def reset(self):
		self.episodes += 1

	def step(self, obs):
		#everything happens here
		if self.old_act!=-1:
			self.actions[self.old_act].update(obs.reward)

		j = np.argmax([act.mean for act in self.actions])

		function_id = self.actions[j].a_id

		#print(self.action_spec)

		args = [[np.random.randint(0, size) for size in arg.sizes]
			for arg in self.action_spec.functions[function_id].args]

		print(args)

		self.old_act=j

		return actions.FunctionCall(function_id, args)

class Action:
	def __init__(self, a_id):
		self.a_id = a_id
		self.mean = 1 #mean of reward (optimistic)
		self.N = 1 #steps

	def update(self, x):
		print(self.a_id,self.mean)
		self.N +=1
		self.mean = (1 - 1/self.N)*self.mean + (1/self.N)*x
