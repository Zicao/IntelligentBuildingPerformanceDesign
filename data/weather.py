'''
Zhichao Tian, AllRight Perserved. Email: tzchao123@qq.com
'''
from AIBPD.__init__ import currentUrl
import os
import re
import numpy as np
import pandas as pd
class Weather():
	'''
	get climate attributes from E+ weather files which comes from ASHRAE fundamental. You may refer ASHRAE 
		fundamental 2017 for more explaination of these attributes.
	'''
	weatherAttributesList=['heatingDB','coolingDB','coolingMCWB','CDD18','HDD5'] 
	weatherDataPath=currentUrl+'\\resources\\weatherData'
	weatherDataDF=pd.DataFrame()
	def __init__(self):
		#self.collectWeatherAttributesIntoWeatherDatDF()
		pass
	
	def collectWeatherAttributesIntoWeatherDatDF(self):
		'''
		collect weather data, and save them into self.weatherDataDF, a attributes of weather class.
		Args:
			None
		'''
		filePath=self.weatherDataPath
		weatherAttributesValueDict={}
		for i in self.weatherAttributesList:
			weatherAttributesValueDict[i]=[]
		cityList=[]
		for weatherFile in os.listdir(filePath):
			cityName='None'
			if re.search('_(\w+)_(.+?)\.\d',weatherFile):
				cityName=re.search('_(\w+)_(.+?)\.\d',weatherFile).group(2)
			weatherAttributesDict=self.getWeatherAttributes(filePath+'\\'+weatherFile+'\\'+weatherFile+'.stat')
			
			for attributes in self.weatherAttributesList:
				weatherAttributesValueDict[attributes].append(weatherAttributesDict[attributes])
			cityList.append(cityName)
		self.weatherDataDF=pd.DataFrame(weatherAttributesValueDict,index=cityList)

	def collectWeatherAttributesIntoDataDF(self,dataDF):
		'''
		collect weather data for cities in exist database (dataDF).
		'''
		cityList=dataDF['city'].values
		uniqueCityList=list(set(cityList))

		weatherDataList=[]
		weatherAttributesValueDict={}
		for i in self.weatherAttributesList:
			weatherAttributesValueDict[i]=[]

		for city in cityList:
			for weatherFile in os.listdir(self.weatherDataPath):
				if re.search(city,weatherFile,re.I):
					weatherAttributesDict=self.getWeatherAttributes(self.weatherDataPath+'\\'+weatherFile+'\\'+weatherFile+'.stat')
					for key in weatherAttributesDict.keys():
						weatherAttributesValueDict[key].append(weatherAttributesDict[key])

		for attributes in self.weatherAttributesList:
			dataDF[attributes]=pd.Series(weatherAttributesValueDict[attributes])

	def addWeatherAttributesIntoDataDFByCity(self,dataDF):
		'''
		add self.weatherAttributes into database DataFrame object by city.
		Args:
			dataDF, existing database object
		'''
		m,n=dataDF.shape
		weatherAttributesDict={}
		for attributes in self.weatherAttributesList:
			weatherAttributesDict[attributes]=[]
		matched=False
		for city in dataDF['city']:
			i=0
			for cityInWea in self.weatherDataDF['city']:
				indexofRow=self.weatherDataDF.index[i]
				if re.search(city,cityInWea,re.I):
					for attributes in self.weatherAttributesList:
						weatherAttributesDict[attributes].append(self.weatherDataDF[attributes][indexofRow])
					matched=True
				i+=1
			if not matched:
				for attributes in self.weatherAttributesList:
					weatherAttributesDict[attributes].append(np.nan)
		for attributes in self.weatherAttributesList:
			dataDF[attributes]=pd.Series(weatherAttributesDict[attributes])


	def extendWeatherData(self,cityList):
		'''
		Sometime, users cannot find a useful weather data. As a result, he may use other weather data that near this building.
		'''
		pass

	def writeWeatherData2CSV(self,weatherDataDF):
		'''
		write weather data attributes into a csv file.
		Args:
			
		'''
		weatherDataDF.to_csv(self.weatherDataPath+'\\weatherAttributes2.csv')

	def readWeatherDataFromCSV(self, csvFile, weatherAttributesList=None):
		'''
		read weather file from a csv file.
		Args:
			csvFile, a csv file containing various building attributes.
			weatherAttributesList, a list object containing building weather attributes such as HDD10. For example
				weatherAttributesList=['heatingDB996','coolingDB04','coolingMCWB04','CDD18','HDD10','RadAvg']

		Return:
			weatherDataDF, a DataFrame object that contain all usefull attributes.
		'''
		if not weatherAttributesList:
			weatherAttributesList=self.weatherAttributesList
		nonvalidAttributes=[]
		self.weatherDataDF=pd.read_csv(csvFile)
		for attributes in self.weatherDataDF.columns:
			if attributes not in self.weatherAttributesList:
				nonvalidAttributes.append(attributes)
		return self.weatherDataDF.drop(nonvalidAttributes,axis=1)

	def downloadWeatherData(self,cityName,ID=''):
		'''
		If cannot find a weather file in local, download weather file into local disk.
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
		bigLine=''
		with open(fileName,'r',encoding='utf-8',errors='ignore') as txt_files:
			for line in txt_files:
				line=re.sub(r'\n',"",line)
				bigLine+=(line)
			bigLine_utf8=bigLine.encode('utf-8')
		if re.search('Heating\sDB(.+)Cooling\sDB'.encode('utf8'),bigLine_utf8,re.S):
			heatingData=re.search('Heating\sDB(.+)Cooling\sDB'.encode('utf8'),bigLine_utf8,re.S).group(1)
			heatingNumbers=re.findall('-?\d+\\.\d+'.encode('utf8'),heatingData)
			if len(heatingNumbers)>=2:
				weatherAttributesDict['heatingDB996']=heatingNumbers[1].decode('utf8')
		else:
			weatherAttributesDict['heatingDB996']=np.nan

		if re.search('Cooling\sDB(.+)DesignStat'.encode('utf8'),bigLine_utf8,re.S):
			coolingData=re.search('Cooling\sDB(.+)DesignStat'.encode('utf8'),bigLine_utf8,re.S).group(1)
			coolingNumbers=re.findall('-?\d+\\.\d+'.encode('utf8'),coolingData)
			if len(coolingNumbers)>=4:
				weatherAttributesDict['coolingDB04']=coolingNumbers[2].decode('utf8')
				weatherAttributesDict['coolingMCWB04']=coolingNumbers[3].decode('utf8')
		else:
			weatherAttributesDict['coolingDB04']=np.nan
			weatherAttributesDict['coolingMCWB04']=np.nan

		if re.search('Monthly\sStandard\sHeating(.+)HDD\sbase\s18\.3'.encode('utf8'),bigLine_utf8,re.S):
			HDDData=re.search('Monthly\sStandard\sHeating(.+)HDD\sbase\s18\.3'.encode('utf8'),bigLine_utf8,re.S).group(1)
			HDDNumbers=re.findall('\d+'.encode('utf8'),HDDData)
			if len(HDDNumbers)>=2:
				weatherAttributesDict['HDD10']=HDDNumbers[1].decode('utf8')
		else:
			weatherAttributesDict['HDD10']=np.nan

		if re.search('CDD\sbase\s18\.3C(.+)CDH\sbase\s23\.3C'.encode('utf8'),bigLine_utf8,re.S):
			CDDData=re.search('CDD\sbase\s18\.3C(.+)CDH\sbase\s23\.3C'.encode('utf8'),bigLine_utf8,re.S).group(1)
			CDDNumbers=re.findall('\d+'.encode('utf8'),CDDData)
			if len(CDDNumbers)>=1:
				weatherAttributesDict['CDD18']=CDDNumbers[0].decode('utf8')
		else:
			weatherAttributesDict['CDD18']=np.nan

		if re.search('Monthly\sStatistics\sfor\sSolar\sRadiation(.+)Maximum\sDirect\sNormal'.encode('utf8'),bigLine_utf8,re.S):
			RadAvgTxt=re.search('Monthly\sStatistics\sfor\sSolar\sRadiation(.+)Maximum\sDirect\sNormal'.encode('utf8'),bigLine_utf8,re.S).group(1)
			if re.search('Global\sAvg\s+(\d+)'.encode('utf8'),RadAvgTxt):
				weatherAttributesDict['RadAvg']=re.search('Global\sAvg\s+(\d+)'.encode('utf8'),RadAvgTxt).group(1).decode('utf8')
		else:
			weatherAttributesDict['RadAvg']=np.nan
		return weatherAttributesDict

if __name__ == '__main__':
	dataSE=pd.Series(['wuxi','nanjing','xuzhou'])
	dataDF=pd.DataFrame()
	dataDF['city']=dataSE
	weather=Weather()
	weather.readWeatherDataFromCSV(weather.weatherDataPath+'\\weatherAttributes.csv')
	weather.addWeatherAttributesIntoDataDFByCity(dataDF)
	print(dataDF)
