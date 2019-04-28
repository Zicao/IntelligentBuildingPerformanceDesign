'''
Copyright Zhichao Tian, E-mail: tzchao123@qq.com.
'''

#fill white in the building. Then, the plan image can be used to recognize the outline (contours).
import cv2
import numpy as np
class FillPlanImage():
	#fill white in the building. Then, the plan image can be used to recognize the outline (contours).
	imgPath='H:\Codes\IntelligentBuildingPerformanceDesign\\resources\detect.jpg'
	def __init__(self):
		pass

	def openImg(self,imgPath):
		img = cv2.imread(imgPath)
		return img

	def fillWhite(self, image):
		'''
		
		'''
		