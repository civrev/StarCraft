'''
to install my StarCraft2 AI stuff so I can run it
'''


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from setuptools import setup

setup(
    name='cwatts',
    version='0.1',
    description='Starcraft II environment agents for civrev',
    author='civrev',
    author_email='none@dot.com',
    license='Yo none',
    keywords='StarCraft AI',
    url='https://github.com/civrev/StarCraft',
    packages=[
        'cwatts',
	'cwatts.agents',
	'cwatts.replay_ripper'
    ],
    install_requires=[

    ],
    entry_points={

    },
    classifiers=[
        'Programming Language :: Python :: 3.4',
    ],
)
