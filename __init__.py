'''

'''
import sys
import os
#if (sys.version_info[0] == 2) and (sys.version_info[1] < 6):
	#raise ImportError("Python Version 2.6 or above is required for SymPy.")
    # Here we can also check for specific Python 3 versions, if needed
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
print(parentUrl)

#把某个文件夹路径添加到path下，以引入该目录下的模块
sys.path.append(parentUrl)


from IntelligentBuildingPerformanceDesign.utility import *
from IntelligentBuildingPerformanceDesign.AIBPD import *

del sys
del os