'''
to install my StarCraft2 AI stuff
so I can run things as a module
run
python3 setup.py install
'''


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from setuptools import setup

setup(
    name='ungsc2',
    version='0.2',
    description='Starcraft II environment agents for UNG',
    author='civrev',
    author_email='civrev@gmail.com',
    license='GNU General Public License v3.0',
    keywords='StarCraft AI',
    url='https://github.com/civrev/StarCraft',
    packages=[
        'ungsc2',
	'ungsc2.agents',
	'ungsc2.replay_ripper'
    ],
    install_requires=[

    ],
    entry_points={

    },
    classifiers=[
        'Programming Language :: Python :: 3.4',
    ],
)
