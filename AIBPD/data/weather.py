'''
Zhichao Tian, AllRight Perserved. Email: tzchao123@qq.com
'''
from IntelligentBuildingPerformanceDesign.__init__ import currentUrl
import os
import re
import numpy as np
class weather():
	'''
	get whether data for famous weather data file, such as epw.
	'''
	weatherAttributesList=['dryBulbTemp']
	weatherDataPath=currentUrl+'\\resources\\weatherData'
	def __init__(self):
		pass

	def addWeatherData(self,dataDF,attributesList):
		'''
		add weather data to temporary data file (DataFrame format) based on their names list.
		Args:
			attributesList, a list object containing weather attributes such as annual average dry-bulb temperature.
		'''
		weatherFileList=os.listdir(weatherDataPath)
		dryBulbTempList=[]
		for city in dataDF['city']:
			#Check whether the weather data of 'city' in local weather data file, If not, download the file.
			for file in weatherFileList:
				if re.search(city,file,re.I):
					dryBulbTempList.append(self.getWeatherAttributes(file,dryBulbTemp))
		pass
	def addWeatherData2Database(self,database):
		'''
		add weather data attributes into database which has a csv format.
		Args:
			database
		'''

		pass
	def downloadWeatherData(self,cityName='Nanjing'):
		'''
		download weather file into local.
		Args:
			cityName, the name of a city.
		'''
		pass
	def getWeatherAttributes(self,fileName):
		'''
		Extract weather attributes from weather files such as dry-bulb temperature.
		Args：
			fileName, the weather file name.
		Return:
			a dict containing weather attributes and their values.
		'''
		weatherAttributesDict={}
		with open(fileName) as weatherFile:
			csvFile=csv.reader(weatherFile,delimiter=',')
			for weatherAttributes in self.weatherAttributesList:
				for row in csvFile:
					for item in row:
						#if find the value in epw file or ddy file save it into a dict
						if re.search(weatherAttributes,item): #this should be revised
							weatherAttributesDict[weatherAttributes]=value
			if not weatherAttributesDict[weatherAttributes]:
				weatherAttributesDict[weatherAttributes]=np.NaN
		return weatherAttributesDict



