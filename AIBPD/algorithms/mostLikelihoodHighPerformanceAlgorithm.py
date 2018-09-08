'''
# Copyright (c) 2013-2018, Zhichao Tian <zhichao.tian@foxmail.com> 
'''


import numpy as np

class highPerformanceByRatio():
	'''
	this algorithm aims at finding out the most likelihood high performance 
	building components, such as heating system and wall construction. 
	We define that high performance component for instance cooling system has the largest
		percentage in the high performance buildings. Proportion = m/n, where
		m is the occurred times of this system in high performance buildings, 
		n is the number of high performance buildings.
		Even this method is simple, but it unveils important information.
	'''
	
