import os
import time
import re
import shutil
import math
import csv
from xpinyin import Pinyin#convert mandarin（普通话） to pinyin(拼音)
import numpy as np
def getWWRNumbers(simulationReport):
	wwrData=[]
	if re.search('\d{1,2}\\.?\d*\s*外窗(.{100})'.encode('utf8'),simulationReport):
		wwrTxt=re.search('\d{1,2}\\.?\d*\s*外窗(.{100})'.encode('utf8'),simulationReport).group(0)
		wwrData=re.findall('0\\.\d+'.encode('utf8'),wwrTxt)
	return wwrData
	
def getWinHTC(simulationReport):
	pass
def getSC(simulationReport):
	pass

def pattern(winListValue):
	patternID3=0
	patternID2=0
	patternID4=0
	patternID5=0
	
	#[0.7, 2.3, 0.63, 0.63, 2.3, 0.74, 0.63, 2.3, 0.58,0.63,2.3,0.27]
	for i in range(1,len(winListValue)-3):
		if winListValue[i]>1.0 and winListValue[i+1]<1.0 and winListValue[i-1]<1.0 and winListValue[i+2]<1.0 and winListValue[i+3]>1.0:
			patternID2+=1
	#[0.7, 0.63, 0.74, 0.58,2.3, 0.74,2.3, 0.74,2.3, 0.74,2.3, 0.74]
	for i in range(3,len(winListValue)-5):
		if winListValue[i-1]<1.0 and winListValue[i-2]<1.0 and winListValue[i]>1.0 and winListValue[i+1]<1.0 and winListValue[i+2]>1.0 and winListValue[i+3]<1.0 and winListValue[i+4]>1.0 and winListValue[i+5]<1.0:
			patternID3+=1
	#[0.7, 2.3, 0.63, 2.3, 0.74, 2.3, 0.58,2.3, 0.27, 0.27, 0.27, 0.27]
	for i in range(len(winListValue)-7):
		if winListValue[i]<1.0 and winListValue[i+1]>1.0 and winListValue[i+2]<1.0 and winListValue[i+3]>1.0 and winListValue[i+4]<1.0 and winListValue[i+5]>1.0 and winListValue[i+6]<1.0 and winListValue[i+7]>1.0:
			patternID4+=1
	#[0.7, 0.63, 0.74, 0.58, 2.3, 2.3, 2.3, 2.3, 0.27, 0.27, 0.27, 0.27]
	for i in range(3,len(winListValue)-5):
		if winListValue[i-1]<1.0 and winListValue[i-2]<1.0 and winListValue[i]>1.0 and winListValue[i+1]>1.0 and winListValue[i+2]>1.0 and winListValue[i+3]>1.0 and winListValue[i+4]<1.0 and winListValue[i+5]<1.0:
			patternID5+=1
	if patternID2>=1:
		return 2
	if patternID3>=1:
		return 3
	if patternID4>=1:
		return 4
	if patternID5>=1:
		return 5
def sameWinIn4Facade(winListValue):
	patternID=0
	pattern=0
	subPattern=0
	HTCList=[]
	wwrList=[]
	for i in winListValue:
			if i>1.0 and i<3.5:
				HTCList.append(i)
			elif i<1.0:
				wwrList.append(i)
	SCKey,SCCount=valueCount(wwrList)
	HTCKey,HTCCount=valueCount(HTCList)
	if SCCount>=3 and HTCCount>=3:
		pattern=True
	else:
		pattern=False
def getWindowNumber(winNumberList):
	winListValue=[]
	for i in winNumberList:
		if float(i)>0 and float(i)<3.5:
			winListValue.append(float(i))
	#verify the datamodel
	print("winListValue",winListValue)
	wwrList=[]
	HTCList=[]
	SCList=[]
	patternID=sameWinIn4Facade(winListValue)
	if patternID:
		for i in winListValue:
			if i>1.0 and i<3.5:
				HTCList.append(i)
			elif i<1.0:
				wwrList.append(i)
		SCKey,SCCount=valueCount(wwrList)
		SCList=[SCKey,SCKey,SCKey,SCKey]
		HTCKey,HTCCount=valueCount(HTCList)
		HTCList=[HTCKey,HTCKey,HTCKey,HTCKey]
		if SCList:
			wwrListN=[]
			for i in wwrList:
				if abs(SCKey-i)>=0.01:
					wwrListN.append(i)
			wwrList=wwrListN
		print("pattern 1")
	elif len(winListValue)>=8:
		#[0.7, 2.3, 0.63, 0.63, 2.3, 0.74, 0.63, 2.3, 0.58,0.63,2.3,0.27]
		if pattern(winListValue)==2:
			front=True
			for i in range(1,len(winListValue)-1):
				if winListValue[i]>1.0 and winListValue[i-1]<1.0 and winListValue[i+1]<1.0:
					wwrList.append(winListValue[i-1])
					HTCList.append(winListValue[i])
					SCList.append(winListValue[i+1])
			HTCList=winSame(HTCList)
			SCList=winSame(SCList)
			print("pattern 2")
		#[0.11, 0.66, 0.56, 0.88, 2.6, 0.4, 2.6, 0.4, 2.6, 0.4, 2.6, 0.4]
		#[0.7, 0.63, 0.74, 0.58,  2.3, 0.74,2.3, 0.74,2.3, 0.74,2.3, 0.74]
		elif pattern(winListValue)==3:
			for i in range(len(winListValue)-1):
				if winListValue[i]>1.0 and winListValue[i+1]<1.0:
					HTCList.append(winListValue[i])
					SCList.append(winListValue[i+1])
				elif winListValue[i]<1.0:
					wwrList.append(winListValue[i])
			HTCList=winSame(HTCList)
			SCList=winSame(SCList)
			print("pattern 3")
		#[0.7, 2.3, 0.63, 2.3, 0.74, 2.3, 0.58,2.3, 0.27, 0.27, 0.27, 0.27]
		elif pattern(winListValue)==4:
			front=True
			for i in range(len(winListValue)-1):		
				if winListValue[i]<1.0 and winListValue[i+1]>1.0:
					wwrList.append(winListValue[i])
					HTCList.append(winListValue[i+1])
				elif winListValue[i]<1.0:
					SCList.append(winListValue[i])
			HTCList=winSame(HTCList)
			SCList=winSame(SCList)
			print("pattern 4")
		#[0.7, 0.63, 0.74, 0.58, 2.3, 2.3, 2.3, 2.3, 0.27, 0.27, 0.27, 0.27]
		elif pattern(winListValue)==5:
			front=True
			for i in range(len(winListValue)):
				if winListValue[i]<1.0 and front:
					wwrList.append(winListValue[i])
				elif winListValue[i]>1.0:
					HTCList.append(winListValue[i])
					if i<=(len(winListValue)-4):
						if winListValue[i]>1.0 and winListValue[i+1]>1.0 and winListValue[i+2]>1.0 and winListValue[i+3]>1.0:
							front=False
				elif winListValue[i] <1.0 and not front:
					SCList.append(winListValue[i])
			HTCList=winSame(HTCList)
			SCList=winSame(SCList)
			print("pattern 5")
		#0.14 0.17 0.18 0.16 2.44 0.35 2.44 0.35 2.44 0.35 2.44 0.35
		elif winListValue[0]<1.0 and winListValue[2]<1.0 and winListValue[3]<1.0 and winListValue[4]<1.0 and winListValue[5]>1.0 and winListValue[6]<1.0:
			wwrList.append(winListValue[0])
			wwrList.append(winListValue[1])
			wwrList.append(winListValue[2])
			wwrList.append(winListValue[3])
			front=False
			for i in range(4,len(winListValue)):
				if winListValue[i]>1.0 and not front:
					HTCList.append(winListValue[i])
					front=True
				elif front and winListValue[i]<1.0:
					SCList.append(winListValue[i])
					front=False
			HTCList=winSame(HTCList)
			SCList=winSame(SCList)
			print("pattern 6")
		#[0.37, 0.48, 3.0, 0.55, 2.0, 2.0, 0.54, 2.0, 2.0, 3.07, 0.84, 2.0, 0.97, 1.06, 0.95, 1.06, 2.92, 2.5, 1.96, 0.1, 3.2, 0.3, 0.41, 3.2, 0.3, 0.1, 3.2, 0.3, 0.26, 3.2]
		else:
			for i in winListValue:
				if i>1.0 and i<3.5:
					HTCList.append(i)
				elif i<1.0:
					wwrList.append(i)
			HTCKey,HTCCount=valueCount(HTCList)
			HTCList=[HTCKey,HTCKey,HTCKey,HTCKey]
			SCKey,SCCount=valueCount(wwrList)
			SCList=[SCKey,SCKey,SCKey,SCKey]
			if SCList:
				wwrListN=[]
				for i in wwrList:
					if not SCList[0]==i:
						wwrListN.append(i)
				wwrList=wwrListN
			
			print("pattern 7")

	else:
		for i in winListValue:
			if i>1.0 and i<3.5:
				HTCList.append(i)
			elif i<1.0 and i>0.0:
				wwrList.append(i)
		SCKey,SCCount=valueCount(wwrList)
		SCList=[SCKey,SCKey,SCKey,SCKey]
		HTCKey,HTCCount=valueCount(HTCList)
		HTCList=[HTCKey,HTCKey,HTCKey,HTCKey]
		if SCList:
			wwrListN=[]
			for i in wwrList:
				if not SCList[0]==i:
					wwrListN.append(i)
			wwrList=wwrListN
		print("pattern 8")
	return wwrList,HTCList,SCList
	
def getThermalNumbers(ThermalSummaryTable):
	windowNumbers=[]
	HTCNumbers=[]
	wwrNumbers=[]
	SCNumbers=[]
	windowdata=None
	if re.search('方\s*?向(.+)?计算软'.encode('utf8'),ThermalSummaryTable,re.S):
		windowdata=re.search('方\s*?向(.+)?计算软'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		windowNumbers=re.findall('\d{1}\\.\d+'.encode('utf8'),windowdata)
	elif re.search('外\s*窗(.+?)计算软'.encode('utf8'),ThermalSummaryTable,re.S) and not len(windowNumbers)>=8:
		windowdata=re.search('外\s*窗(.+?)计算软'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		windowNumbers=re.findall('\d{1}\\.\d+'.encode('utf8'),windowdata)
	elif re.search('方\s*?向(.+)?天\s*窗'.encode('utf8'),ThermalSummaryTable,re.S) and not len(windowNumbers)>=8:
		windowdata=re.search('方\s*?向(.+)?天\s*窗'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		windowNumbers=re.findall('\d{1}\\.\d+'.encode('utf8'),windowdata)
	elif re.search('外\*窗(.+)?天\s*窗'.encode('utf8'),ThermalSummaryTable,re.S) and not len(windowNumbers)>=8:
		windowdata=re.search('外\s*窗(.+)?天\s*窗'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		windowNumbers=re.findall('\d{1}\\.\d+'.encode('utf8'),windowdata)
	elif re.search('窗墙面积比(.+)?计算软'.encode('utf8'),ThermalSummaryTable,re.S) and not len(windowNumbers)>=8:
		windowdata=re.search('窗墙面积比(.+)?计算软'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		windowNumbers=re.findall('\d{1}\\.\d+'.encode('utf8'),windowdata)
	elif re.search('窗墙面积(.+)?遮阳系数'.encode('utf8'),ThermalSummaryTable,re.S) and re.search('遮阳系数.+(\d{1}\\.\d*)\s*(\d{1}\\.\d*)\s*(\d{1}\\.\d*)\s*(\d{1}\\.\d*)'.encode('utf8'),ThermalSummaryTable,re.S) and not len(windowNumbers)>=8:
		windowdata=re.search('窗墙面积(.+)?遮阳系数'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		windowSC=re.search('遮阳系数.+(\d{1}\\.\d*)\s*(\d{1}\\.\d*)\s*(\d{1}\\.\d*)\s*(\d{1}\\.\d*)'.encode('utf8'),ThermalSummaryTable,re.S)
		windowdata=windowdata+windowSC.group(0)
		windowNumbers=re.findall('\d{1}\\.\d+'.encode('utf8'),windowdata)
	elif re.search('积比(.+)?计算软'.encode('utf8'),ThermalSummaryTable,re.S) and not len(windowNumbers)>=8:
		windowdata=re.search('积比(.+)?计算软'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		windowNumbers=re.findall('\d{1}\\.\d+'.encode('utf8'),windowdata)
	elif re.search('非周边地面(.+)?计算软'.encode('utf8'),ThermalSummaryTable,re.S) and not len(windowNumbers)>=8:
		windowdata=re.search('非周边地面(.+)?计算软'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		windowNumbers=re.findall('\d{1}\\.\d+'.encode('utf8'),windowdata)
	if len(windowNumbers)<8:
		print("error in match data of windowdata ThermalSummaryTable")
		windowdata=ThermalSummaryTable
		windowNumbers=re.findall('(\d{1}\\.\d+)'.encode('utf8'),windowdata)

	
	if re.search('传热系数(.+)遮阳系数'.encode('utf8'),ThermalSummaryTable,re.S):
		HTCData=re.search('传热系数(.+)遮阳系数'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		HTCNumbers=re.findall('\d{1}\\.\d*'.encode('utf8'),HTCData)
	else:
		HTCData=None
	
	if re.search('积比\s*(0\\.\d{2})\s*?(0\\.\d{2})\s*?(0\\.\d{2})\s*?(0\\.\d{2})'.encode('utf8'),ThermalSummaryTable,re.S):
		wwrData=re.search('积比\s*?(0\\.\d{2})\s*?(0\\.\d{2})\s*?(0\\.\d{2})\s*?(0\\.\d{2})'.encode('utf8'),ThermalSummaryTable,re.S)
		wwrNumbers.append(wwrData.group(1))
		wwrNumbers.append(wwrData.group(2))
		wwrNumbers.append(wwrData.group(3))
		wwrNumbers.append(wwrData.group(4))
	elif re.search('窗墙面积(.+)传热系数'.encode('utf8'),ThermalSummaryTable,re.S):
		wwrData=re.search('窗墙面积(.+)传热系数'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		wwrNumbers=re.findall('\d{1}\\.\d*'.encode('utf8'),wwrData)
	else:
		wwrData=None
		
	if re.search('遮阳系数\s*SC\*(0\\.\d{2})\s*(0\\.\d{2})\s*(0\\.\d{2})\s*(0\\.\d{2})'.encode('utf8'),ThermalSummaryTable,re.S):
		SCData=re.findall('遮阳系数\s*SC\*(0\\.\d{2})\s*(0\\.\d{2})\s*(0\\.\d{2})\s*(0\\.\d{2})'.encode('utf8'),ThermalSummaryTable,re.S)
		SCNumbers=re.findall('\d{1}\\.\d*'.encode('utf8'),SCData)
	else:
		SCData=None
	return windowNumbers,HTCNumbers,wwrNumbers,SCNumbers,windowdata

def getEnclosureDataFromSimulationReport(simulationReport):
	'''
	get data from simulation report. If there are errors in getting enclosure data from the 
	thermal summary report, this function will provide some supplemental data.
	'''
	WWR_West=0.0
	WWR_East=0.0
	WWR_North=0.0
	WWR_South=0.0
	ExWindowHTC_North=0.0
	ExWindowHTC_South=0.0
	ExWindowHTC_West=0.0
	ExWindowHTC_East=0.0
	SC_North=0.0
	SC_South=0.0
	SC_West=0.0
	SC_East=0.0
	RoofHTC=0.0
	ExWallHTC=0.0
	OverheadFloorHTC=0.0
	FloorHTCOuter=0.0
	windowNumbers=[]
	WindowDataString='nothing'.encode('utf8')

	if re.search('窗墙比(.*?)0\.70\s*符合'.encode('utf8'),simulationReport):
		WindowDataString=re.search('窗墙比(.*?)0\.70\s*符合'.encode('utf8'),simulationReport).group(0)
	elif re.search('遮阳系数(.*)0\.70'.encode('utf8'),simulationReport):
		WindowDataString=re.search('遮阳系数(.*)0\.70'.encode('utf8'),simulationReport).group(0)
	elif re.search('遮阳系数(.*)0\.70'.encode('utf8'),simulationReport):
		WindowDataString=re.search('遮阳系数(.*)0\.70'.encode('utf8'),simulationReport).group(0)
	elif re.search('窗墙比(.*?)建筑外窗气密'.encode('utf8'),simulationReport):
		WindowDataString=re.search('窗墙比(.*?)建筑外窗气密'.encode('utf8'),simulationReport).group(0)

	windowValues=re.findall('\d{1}\\.\d*'.encode('utf8'),WindowDataString)
	print('windowValues',windowValues)

def filtrateWWR(ThermalSummaryTable):
	#南北东西
	if re.search('南.*北.*东.*西'.encode('utf8'),ThermalSummaryTable):
		return 1
	#东西南北
	elif re.search('东.*西.*南.*北'.encode('utf8'),ThermalSummaryTable):
		return 2
	#东南西北
	elif re.search('东.*南.*西.*北'.encode('utf8'),ThermalSummaryTable):
		return 3
	#北东西南
	elif re.search('东.*北.*西.*南'.encode('utf8'),ThermalSummaryTable):
		return 4
	else:
		return 0
def arrageWinData(winList,winPattern):
	'''
	
	'''
	newList=[]
	if winPattern==1:
		if len(winList)>=4:
			newList.append(winList[2])
			newList.append(winList[3])
			newList.append(winList[0])
			newList.append(winList[1])
		elif len(winList)==3:
			newList.append(winList[2])
			newList.append(np.nan)
			newList.append(winList[0])
			newList.append(winList[1])
		elif len(winList)==2:
			newList.append(winList[0])
			newList.append(winList[1])
			newList.append(np.nan)
			newList.append(np.nan)
		elif len(winList)==1:
			newList.append(winList[0])
			newList.append(np.nan)
			newList.append(np.nan)
			newList.append(np.nan)
		else:
			newList.append(np.nan)
			newList.append(np.nan)
			newList.append(np.nan)
			newList.append(np.nan)
	elif winPattern==2:
		if len(winList)>=4:
			newList=winList[:4]
		elif len(winList)==3:
			newList=winList[:3]
			newList.append(np.nan)
		elif len(winList)==2:
			newList=winList[:2]
			newList.append(np.nan)
			newList.append(np.nan)
		elif len(winList)==1:
			newList.append(winList[0])
			newList.append(np.nan)
			newList.append(np.nan)
			newList.append(np.nan)
		else:
			newList.append(np.nan)
			newList.append(np.nan)
			newList.append(np.nan)
			newList.append(np.nan)
	elif winPattern==3:
		if len(winList)>=4:
			newList.append(winList[0])
			newList.append(winList[2])
			newList.append(winList[1])
			newList.append(winList[3])
		elif len(winList)==3:
			newList.append(winList[0])
			newList.append(winList[2])
			newList.append(winList[1])
			newList.append(np.nan)
		elif len(winList)==2:
			newList.append(winList[0])
			newList.append(np.nan)
			newList.append(winList[1])
			newList.append(np.nan)
		elif len(winList)==1:
			newList.append(winList[0])
			newList.append(np.nan)
			newList.append(np.nan)
			newList.append(np.nan)
		else:
			newList.append(np.nan)
			newList.append(np.nan)
			newList.append(np.nan)
			newList.append(np.nan)
	else:
		if len(winList)>=4:
			newList=winList[:4]
		elif len(winList)==3:
			newList=winList
			newList.append(np.nan)
		elif len(winList)==2:
			newList=winList
			newList.append(np.nan)
			newList.append(np.nan)
		elif len(winList)==1:
			newList.append(winList[0])
			newList.append(np.nan)
			newList.append(np.nan)
			newList.append(np.nan)
		else:
			newList.append(np.nan)
			newList.append(np.nan)
			newList.append(np.nan)
			newList.append(np.nan)
	return newList

def toDigital(list1):
	list2=[]
	for i in list1:
		list2.append(float(i))
	return list2

def valueCount(valueList):
	'''
	return the most often used number
	'''
	uniqueValue = list(set(valueList))
	uniqueValueDict={}
	for i in uniqueValue:
		count=0
		for j in valueList:
			if i==j:
				count+=1
		uniqueValueDict[i]=count
	#find the highest count and its key

	maxCount=0
	maxKey=0.0
	valuekeys=uniqueValueDict.keys()
	for i in valuekeys:
		if uniqueValueDict[i]>maxCount:
			maxCount=uniqueValueDict[i]
			maxKey=i
	return maxKey, maxCount
def winSame(valueList):
	maxKey, maxCount=valueCount(valueList)
	if maxCount==4:
		return [maxKey,maxKey,maxKey,maxKey]
	elif len(valueList)>4:
		return valueList[-5:-1]
	else:
		return valueList
		
def getposition(winListValue):
	position1=[]
	for i in range(len(winListValue)):
		if winListValue[i]>2.0 and winListValue[i]<3.5:
			position1.append(i)
		else:
			winListValue.remove(winListValue[i])
	if position1:
		return max(position1),min(position1)
	elif len(position1)>=12:
		return 4,7
	else:
		return None,None
def getWWR(simulationReport):

	'''
	get wwr from simulation report. double check this value with previous wwr data
	'''
	wwrData1=[]
	wwrData2=[]
	wwrTxt1='nothing'.encode('utf8')
	wwrTxt2='nothing'.encode('utf8')
	if re.search('窗墙比(.+)窗墙比(.+)'.encode('utf8'),simulationReport):
		wwrTxt1=re.search('窗墙比(.+)窗墙比(.+)'.encode('utf8'),simulationReport).group(1)
		wwrTxt2=re.search('窗墙比(.+)窗墙比(.+)'.encode('utf8'),simulationReport).group(2)
	elif re.search('窗墙比(.{100})'.encode('utf8'),simulationReport):
		wwrTxt1=re.search('窗墙比(.{100})'.encode('utf8'),simulationReport).group(1)

	wwrData1=re.findall('0\\.\d{2}'.encode('utf8'),wwrTxt1)
	wwrData2=re.findall('0\\.\d{2}'.encode('utf8'),wwrTxt2)
	return wwrData1,wwrData2

def doubleCheckWWR(wwrList1,wwrList2,wwrList3):
	real_wwr=[]
	for wwr in wwrList2:
		if float(wwr.decode('utf8'))==0.7:
			wwrList2.remove(wwr)
	if len(wwrList2)>=20:
		wwrList2=wwrList2[:21]
	if len(wwrList3)>=20:
		wwrList3=wwrList3[:21]
	'''for wwr in wwrList1:
		if wwr in wwrList2 or wwr in wwrList3:
			real_wwr.append(wwr)'''
	for wwr in wwrList2:
		if wwr in wwrList3 and wwr not in real_wwr:
			real_wwr.append(wwr)
	if len(real_wwr)>=3:
		return real_wwr
	else:
		return wwrList1
