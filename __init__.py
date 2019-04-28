# encoding: utf-8
'''
Artificial Intelligent Building Performance Design module for python.
================================================

AIBPD is a python module conducting various building performance analysis.
At this stage, it aims to fulfill data-driven building performance design.

Connect with Zhichao Tian (zhichao.tian@foxmail.com), if you have any questions or recommendations.
'''
import sys
import os
if (sys.version_info[0] == 2):
	raise ImportError("Python Version 3.0+ is required")
     #Here we can also check for specific Python 3 versions, if needed
global currentUrl
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))

del sys
del os
