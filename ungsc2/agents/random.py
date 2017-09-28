"""A random agent for starcraft, with comments!"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy

from ungsc2.agents import base
from pysc2.lib import actions


#so the RandomAgent class is an extention of the BaseAgent class
class RandomAgent(base.BaseAgent):
	"""A random agent for starcraft, with comments"""
	#so it looks like any agent needs a step function
	#and all step functions should take 2 arguments
	#self, and obs
	#self just lets any instance of the class access that
	#instance's characteristics, not the actual class's
	#obs is short for observations which is something the
	#game API provides
	def step(self, obs):
		#it calls and runs the step function from the base agent
		#which only does about 2 lines of code
		super(RandomAgent, self).step(obs)

		#this just picks a random function from a dictionay/DataFrame
		#it appears that the function id is important here, rather than name
		function_id = numpy.random.choice(obs.observation["available_actions"])

		#this is a deep list comprehender
		#basically what it is saying is
		#for this function (the function_id choosen randomly)
		#go get the attributes of arguments neccissary to use this function
		#for every argument you get, make a random value that is within
		#the range of that argument
		args = [[numpy.random.randint(0, size) for size in arg.sizes]
			for arg in self.action_spec.functions[function_id].args]

		#now it will return the action it wants to run, with parameters
		#so for example it could be
		#1, [64, 64]
		# function_id 1, which is the action move_camera, which takes in a minimap arg
		#the minimap arg is [x,y] position on the minimap to move
		#the camera to
		#meaning it takes 2 arguments the x and y
		#print(function_id, args)
		return actions.FunctionCall(function_id, args)
