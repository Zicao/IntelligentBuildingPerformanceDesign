import os
import time
import re
import shutil
import math
import csv
from xpinyin import Pinyin#convert mandarin（普通话） to pinyin(拼音)
import numpy as np
def getRoofHTC(simulationReport):
	RoofHTC=0.0
	if re.search('\d{1,2}\s*屋顶(.+?)传\s*热\s*系\s*数(.+?)([01]\\.\d+)(.+?)外墙'.encode('utf8'),simulationReport):
		RoofHTC=re.search('\d{1,2}\s*屋顶(.+?)传\s*热\s*系\s*数(.+?)([01]\\.\d+)(.+?)外墙'.encode('utf8'),simulationReport).group(3).decode('utf8')
	elif re.search('\d{1,2}\\.?\d*屋顶(.+?)传\s*热\s*系\s*数(.+?)([01]\\.\d+)(.+?)外墙'.encode('utf8'),simulationReport):
		RoofHTC=re.search('\d{1,2}\\.?\d*屋顶(.+?)传\s*热\s*系\s*数(.+?)([01]\\.\d+)(.+?)外墙'.encode('utf8'),simulationReport).group(3).decode('utf8')
	elif re.search('屋顶传热系数(.+?)([012]\\.\d+)'.encode('utf8'),simulationReport):
		RoofHTC=re.search('屋顶传热系数(.+?)([012]\\.\d+)'.encode('utf8'),simulationReport).group(2).decode('utf8')
	return RoofHTC
def getExWallHTC(simulationReport):
	ExWallHTC=0.0
	if re.search('外墙传热系数(.+?)([012]\\.\d+)'.encode('utf8'),simulationReport):
		ExWallHTC=re.search('外墙传热系数(.+?)([012]\\.\d+)'.encode('utf8'),simulationReport).group(2).decode('utf8')
	elif re.search('\d{1,2}\\.?\d*外墙(.+?)传\s*热\s*系\s*数(.+?)([01]\\.\d+)(.+?)非采暖'.encode('utf8'),simulationReport):
		ExWallHTC=re.search('\d{1,2}\\.?\d*外墙(.+?)传\s*热\s*系\s*数(.+?)([01]\\.\d+)(.+?)非采暖'.encode('utf8'),simulationReport).group(3).decode('utf8')
	elif re.search('\d{1,2}\\.?\d*外墙(.+?)传\s*热\s*系\s*数(.+?)([01]\\.\d+)'.encode('utf8'),simulationReport):
		ExWallHTC=re.search('\d{1,2}\\.?\d*外墙(.+?)传\s*热\s*系\s*数(.+?)([01]\\.\d+)'.encode('utf8'),simulationReport).group(3).decode('utf8')
	elif re.search('外墙平均传热系数(.+?)([012]\\.\d+)'.encode('utf8'),simulationReport):
		ExWallHTC=re.search('外墙平均传热系数(.+?)([012]\\.\d+)'.encode('utf8'),simulationReport).group(2).decode('utf8')
	return ExWallHTC

def getOverheadFloorHTC(simulationReport):
	pass
def getFloorHTC(simulationReport):
	pass


def getEachOpaqueEnclosure(ThermalSummaryTable):
	RoofHTC,ExWallHTC,OverheadFloorHTC,FloorHTCOuter=None,None,None,None
	if re.search('屋\s*面.*?([01]\\.\d+).*外墙'.encode('utf8'),ThermalSummaryTable):
		RoofHTC=re.search('屋\s*面.*?([01]\\.\d+).*外墙'.encode('utf8'),ThermalSummaryTable).group(1).decode('utf8')
	elif re.search('屋\s*面\s*([01]\\.\d+)\s*'.encode('utf8'),ThermalSummaryTable):
		RoofHTC=re.search('屋\s*面\s*([01]\\.\d+)\s*'.encode('utf8'),ThermalSummaryTable).group(1).decode('utf8')
	elif re.search('屋\s*面.{1,5}([01]\\.\d+)\s*'.encode('utf8'),ThermalSummaryTable):
		RoofHTC=re.search('屋\s*面.{1,5}([01]\\.\d+)\s*'.encode('utf8'),ThermalSummaryTable).group(1).decode('utf8')
	elif re.search('平屋面.{1,5}([01]\\.\d+)\s*'.encode('utf8'),ThermalSummaryTable):
		RoofHTC=re.search('平屋面.{1,5}([01]\\.\d+)\s*'.encode('utf8'),ThermalSummaryTable).group(1).decode('utf8')
	else:
		RoofHTC=None

	if re.search('外\s*墙.+?([01]\\.\d+).*底面'.encode('utf8'),ThermalSummaryTable):
		ExWallHTC=re.search('外\s*墙.+?([01]\\.\d+).*底面'.encode('utf8'),ThermalSummaryTable).group(1).decode('utf8')
	elif re.search('主墙体.{1,5}([01]\\.\d+)'.encode('utf8'),ThermalSummaryTable):
		ExWallHTC=re.search('主墙体.{1,5}([01]\\.\d+)'.encode('utf8'),ThermalSummaryTable).group(1).decode('utf8')
	elif re.search('外\s*墙(.+)?底面'.encode('utf8'),ThermalSummaryTable):
		ExWallSection=re.search('外\s*墙(.+)?底面'.encode('utf8'),ThermalSummaryTable).group(1)
		ExWallList=re.findall('([01]\\.\d+)'.encode('utf8'),ExWallSection)
		if ExWallList:
			ExWallHTC=ExWallList[0]
		else:
			ExWallHTC=None
	else:
		ExWallHTC=None

	if re.search('架空.+?([012]\\.\d+).*分隔'.encode('utf8'),ThermalSummaryTable):
		OverheadFloorHTC=re.search('架空.+?([012]\\.\d+).*分隔'.encode('utf8'),ThermalSummaryTable).group(1).decode('utf8')
	elif re.search('底面接触室外(.+)?地面'.encode('utf8'),ThermalSummaryTable):
		OverheadFloorSection=re.search('底面接触室外(.+)?地面'.encode('utf8'),ThermalSummaryTable).group(1)
		OverheadFloorList=re.findall('([012]\\.\d+)'.encode('utf8'),OverheadFloorSection)
		if OverheadFloorList:
			OverheadFloorHTC=OverheadFloorList[0]
		else:
			OverheadFloorHTC=None	
	else:
		OverheadFloorHTC=None

	
	if re.search('周边地面.+?(\d\\.\d+).*非周边地面'.encode('utf8'),ThermalSummaryTable):
		FloorHTCOuter=re.search('周边地面.+?(\d\\.\d+).*非周边地面'.encode('utf8'),ThermalSummaryTable).group(1).decode('utf8')
	elif re.search('地面.+?(\d\\.\d+).*外窗'.encode('utf8'),ThermalSummaryTable):
		FloorHTCOuter=re.search('地面.+?(\d\\.\d+).*外窗'.encode('utf8'),ThermalSummaryTable).group(1).decode('utf8')
	elif re.search('地面(.+)外窗'.encode('utf8'),ThermalSummaryTable):
		FloorHTCOuterSection=re.search('地面(.+)外窗'.encode('utf8'),ThermalSummaryTable).group(1)
		FloorHTCOuterList=re.findall('([012]\\.\d+)'.encode('utf8'),FloorHTCOuterSection)
		if FloorHTCOuterList:
			FloorHTCOuter=FloorHTCOuterList[0]
	elif re.search('地面.+?(\d\\.\d+).*采暖'.encode('utf8'),ThermalSummaryTable):
		FloorHTCOuter=re.search('地面.+?(0\\.\d+).*采暖'.encode('utf8'),ThermalSummaryTable).group(1).decode('utf8')
	else:
		FloorHTCOuter=None

	return RoofHTC,ExWallHTC,OverheadFloorHTC,FloorHTCOuter

def getOpaqueEnclosure(ThermalSummaryTable):
	opaqueEnclosure=None
	opaqueEnclosureV=[]
	if re.search('传热系数(.+?)做\s*法(.+)?外窗'.encode('utf8'),ThermalSummaryTable,re.S):
		opaqueEnclosure=re.search('传热系数(.+?)做\s*法(.+)?外窗'.encode('utf8'),ThermalSummaryTable,re.S).group(2)
		opaqueEnclosureV=re.findall('[012]\\.\d*'.encode('utf8'),opaqueEnclosure)
	if re.search('屋\s*面(.+)?外窗'.encode('utf8'),ThermalSummaryTable,re.S):
		opaqueEnclosure=re.search('屋\s*面(.+)?外窗'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		opaqueEnclosureV=re.findall('[012]\\.\d*'.encode('utf8'),opaqueEnclosure)
	if re.search('屋\s*面(.+)?外\*窗'.encode('utf8'),ThermalSummaryTable,re.S) and (len(opaqueEnclosureV)>=32 or len(opaqueEnclosureV)<=2):
		opaqueEnclosure=re.search('屋\s*面(.+)?外\*窗'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		opaqueEnclosureV=re.findall('[012]\\.\d*'.encode('utf8'),opaqueEnclosure)
	if re.search('屋\s*面(.+)?分隔供暖'.encode('utf8'),ThermalSummaryTable,re.S) and (len(opaqueEnclosureV)>=32 or len(opaqueEnclosureV)<=2):
		opaqueEnclosure=re.search('屋\s*面(.+)?分隔供暖'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		opaqueEnclosureV=re.findall('[012]\\.\d*'.encode('utf8'),opaqueEnclosure)
	if re.search('结构部位(.+)?窗墙面'.encode('utf8'),ThermalSummaryTable,re.S) and (len(opaqueEnclosureV)>=32 or len(opaqueEnclosureV)<=2):
		opaqueEnclosure=re.search('结构部位(.+)?窗墙面'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		opaqueEnclosureV=re.findall('[012]\\.\d*'.encode('utf8'),opaqueEnclosure)
	if re.search('屋面(.+)窗墙面'.encode('utf8'),ThermalSummaryTable,re.S) and (len(opaqueEnclosureV)>=32 or len(opaqueEnclosureV)<=2):
		opaqueEnclosure=re.search('屋面(.+)?窗墙面'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		opaqueEnclosureV=re.findall('[012]\\.\d*'.encode('utf8'),opaqueEnclosure)
	if re.search('做法(.+)传热系数'.encode('utf8'),ThermalSummaryTable,re.S)and (len(opaqueEnclosureV)>=32 or len(opaqueEnclosureV)<=2):
		opaqueEnclosure=re.search('做法(.+)传热系数'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		opaqueEnclosureV=re.findall('[012]\\.\d*'.encode('utf8'),opaqueEnclosure)
	if re.search('做法(.+)'.encode('utf8'),ThermalSummaryTable,re.S)and len(opaqueEnclosureV)<=2:
		opaqueEnclosure=re.search('做法(.+)'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		opaqueEnclosureV=re.findall('[012]\\.\d*'.encode('utf8'),opaqueEnclosure)
	if not opaqueEnclosureV:
		print("error in getting opaqueEnclosure ThermalSummaryTable")
	return opaqueEnclosureV
def getOpaqueEnclosure2(ThermalSummaryTable):
	opaqueEnclosure=None
	opaqueEnclosureV=[]
	if re.search('传热系数(.+?)做\s*法(.+)?外窗'.encode('utf8'),ThermalSummaryTable,re.S):
		opaqueEnclosure=re.search('传热系数(.+?)做\s*法(.+)?外窗'.encode('utf8'),ThermalSummaryTable,re.S).group(2)
		opaqueEnclosureV=re.findall('[012]\\.\d*'.encode('utf8'),opaqueEnclosure)
	elif re.search('屋\s*面(.+)?外窗'.encode('utf8'),ThermalSummaryTable,re.S):
		opaqueEnclosure=re.search('屋\s*面(.+)?外窗'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		opaqueEnclosureV=re.findall('[012]\\.\d*'.encode('utf8'),opaqueEnclosure)
	if re.search('屋\s*面(.+)?外\*窗'.encode('utf8'),ThermalSummaryTable,re.S) and (len(opaqueEnclosureV)>=32 or len(opaqueEnclosureV)<=2):
		opaqueEnclosure=re.search('屋\s*面(.+)?外\*窗'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		opaqueEnclosureV=re.findall('[012]\\.\d*'.encode('utf8'),opaqueEnclosure)
	if re.search('屋\s*面(.+)?分隔供暖'.encode('utf8'),ThermalSummaryTable,re.S) and (len(opaqueEnclosureV)>=32 or len(opaqueEnclosureV)<=2):
		opaqueEnclosure=re.search('屋\s*面(.+)?分隔供暖'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		opaqueEnclosureV=re.findall('[012]\\.\d*'.encode('utf8'),opaqueEnclosure)
	if re.search('结构部位(.+)?窗墙面'.encode('utf8'),ThermalSummaryTable,re.S) and (len(opaqueEnclosureV)>=32 or len(opaqueEnclosureV)<=2):
		opaqueEnclosure=re.search('结构部位(.+)?窗墙面'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		opaqueEnclosureV=re.findall('[012]\\.\d*'.encode('utf8'),opaqueEnclosure)
	if re.search('屋面(.+)窗墙面'.encode('utf8'),ThermalSummaryTable,re.S) and (len(opaqueEnclosureV)>=32 or len(opaqueEnclosureV)<=2):
		opaqueEnclosure=re.search('屋面(.+)?窗墙面'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		opaqueEnclosureV=re.findall('[012]\\.\d*'.encode('utf8'),opaqueEnclosure)
	if re.search('做法(.+)传热系数'.encode('utf8'),ThermalSummaryTable,re.S)and (len(opaqueEnclosureV)>=32 or len(opaqueEnclosureV)<=2):
		opaqueEnclosure=re.search('做法(.+)传热系数'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		opaqueEnclosureV=re.findall('[012]\\.\d*'.encode('utf8'),opaqueEnclosure)
	if re.search('做法(.+)'.encode('utf8'),ThermalSummaryTable,re.S)and len(opaqueEnclosureV)<=2:
		opaqueEnclosure=re.search('做法(.+)'.encode('utf8'),ThermalSummaryTable,re.S).group(1)
		opaqueEnclosureV=re.findall('[012]\\.\d*'.encode('utf8'),opaqueEnclosure)
	if not opaqueEnclosureV:
		print("error in getting opaqueEnclosure ThermalSummaryTable")
	return opaqueEnclosureV