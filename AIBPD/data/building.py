#proposedBuilding
'''
# Copyright (c) 2013-2018, Zhichao Tian <tzchao123@qq.com> 
'''
class Building():

	building={
		'ID': 1,
		'name':'zhongdaHall',
		'city':'Nanjing',
		'zipCode':'210096',
		'address':'sipailou #2',
		'region':1,
			#'JiangSu, Shanghai, Zhejiang' = 1
			#'Henan, Anhui, Shanxi, Hubei, Hunan, JiangXi' = 2
			#'Sichuan, Chongqing, Guizhou, Yunnan, Xizang, Shananxi, Xinjiang, Gansu, Qinghai, Xizang'=3
			#'Guangzhou, Xianggang, Aomen, Fujian, Hainan'=4
			#'Beijing, Tianjin, Hebei' = 5
			#'Heilongjiang, Jilin, Liangning, Neimenggu'=6
		'yearOfConstruction':1930,
		'renovationYear':1980,
		'climateZone': 3, 
			#Very cold=1, 
			#cold=2, 
			#SummerHotWinterCold=3, 
			#SummerHotWinterWarm=4, 
			#Warm=5,
		'CDD65':1500,
		'buildingArea': 10000,	#unit:m2
		'numFloorAbove':4,	#unit:-
		'numFloorBelow':1,	#unit:-
		'buildingShape':2,
			#01' = 'Square'，正方形
			#'02' = 'Wide rectangle',宽方形
			#'03' = 'Narrow rectangle'，窄方形
			#'04' = 'Rectangle or square with an interior courtyard',回型
			#'05' = '"H" shaped'，H型
			#'06' = '"U" shaped'
			#'07' = '"E" shaped'
			#'08' = '"T" shaped'
			#'09' = '"L" shaped'
			#'10' = '"+" or cross shaped'
			#'11' = 'Other shape'
		'principleActivity':2,      
			#'01' = 'Vacant','02' = 'Office','04' = 'Laboratory',
			#'05' = 'Nonrefrigerated warehouse'
			#'06' = 'Food sales','07' = 'Public order and safety',
			#'08' = 'Outpatient health care'
			#'11' = 'Refrigerated warehouse','12' = 'Religious worship'
			#'13' = 'Public assembly','14' = 'Education','15' = 'Food service'
			#'16' = 'Inpatient health care','17' = 'Nursing','18' = 'Lodging'
			#'23' = 'Strip shopping mall','24' = 'Enclosed mall',
			#'25' = 'Retail other than mall'
			#'26' = 'Service','91' = 'Other'
		'WWR':0.2,
		'WWRSouth':0.2,
		'WWRNorth':0.4,
		'WWRWest':0.01,
		'WWREast':0.02,
		'exWinHTC':2.1,
		'exWinHTCSouth':2.1,
		'exWinHTCNorth':2.1,
		'exWinHTCWest':2.1,
		'exWinHTCEast':2.1,
		'exWinAirtightness':6,
		'exDoorAirtightness':3,
		
		'SC':0.41,
		'SCSouth':0.41,
		'SCNorth':0.41,
		'SCWest':0.41,
		'SCEast':0.41,
		'roofHTC':0.6,
		'roofConstruction':1,
			#
			#
			#
			#
			#
		'wallConstruction':1,
			#'brick no insultion' = '1'
			#'light concrete brick wall with insulation' = '2'
			#'brick wall with insulation' = '3'
			#'transparent glass wall' = '4'
			#'Unknown' = '0'
		'exWallHTC':0.8,
		'overHeadFloorHTC':1.2,
		'floorHTC':2.0,
		'exWinAirTightness':6,
		'peoplePerArea':0.2,
		'numPeople':1500,
		'lightingType':1,
			# LED = 1
			# fluorescent = 2
			# incandescent = 3
		'lightingLevel':6.0,
		'pluginEquipLevel':8.0,
		'designHeatingLoad':75.9,
		'designCoolingLoad':116.26,
		'heatingPrimarySys':3, 
			#1' = 'Furnaces'
			#'2' = 'Packaged rooftop central unit'
			#'3' = 'Boilers inside'
			#'4' = 'District steam or hot water'
			#'5' = 'Heat pumps'
			#'6' = 'Individual space heaters'
			#'7' = 'Other heating equipment'
		'coolingPrimarySys':3,
			#'1' = 
			#'2' = 'Packaged air conditioning units'
			#'3' = 'Central chillers inside'
			#'4' = 'District chilled water piped in from outside the building'
			#'5' = 'Heat pumps for cooling'
			#'6' = 'Individual room air conditioners (other than heat pumps)'
			#'7' = '"Swamp" coolers or evaporative coolers'
			#'8' = 'Other cooling equipment'
		'terminal':6,
			#'1' = 'Residential-type wallhang or direct expension heat pump'
			#'2' = 'windowAirConditioner'
			#'3' = 'Radiant fin'
			#'4' = 'baseboard radiant heater'
			#'5' = 'radiant cooling & heating'
			#'6' = 'fancoil'
			#'7' = 'VRV system'
			#'8' = 'single duct uncontrol'
			#'9' = 'CAV'
			#'10' = 'VAV'
			#11 = 'PIU'
		'CWPumpType':1,
			#'1' = 'constant'
			#'2' = 'variable speed'
		'condensorType':1,
			#'1' = 'coolingTower'
			#'2' = 'Air cooled'
		'COOLP':1, #cooling percentage
		'MAINCL':2, #main cooling system
		'MAINHT':2, #main heating system
		'EUICooling':1000000,#cooling energy per square meter
		'HECS':1, #high energy efficient cooling system? ,1: yes, 2: no.
		
		}
	#
	def __init__(self):
		pass
	
	def tran2FitDatabase(self,dict):
		'''
		In order to use a database, the proposedBuilding object should fit this database.
		'''
		pass

	def showAllbuilding(self):
		pass

	def defineBuilding(self,buildingDict):
		#define the proposed building
		'''
		Args:
			buildingDict: used to define the proposed building
		Return:
			self.building
		'''
		proposedDict=buildingDict.keys()
		for i in proposedDict:
			self.building[i]=buildingDict[i]
		return self.building

	def blding4SimilarityAnalysis(self):
		'''
		return:
			a sub-building object.
			An example, prpsedBlding4SmlarAnalysis={'climateZone':3,   'principleActivity':2,
												'buildingArea': 10000, 'yearOfConstruction':1930,
												'buildingShape':2,      'wallConstruction':2,
												'WWR': 0.3,             'peoplePerArea': 0.2}
		'''

		bldingDict={}
		bldingDict['climateZone']=self.building['climateZone']
		bldingDict['principleActivity']=self.building['principleActivity']
		bldingDict['buildingArea']=self.building['buildingArea']
		bldingDict['yearOfConstruction']=self.building['yearOfConstruction']
		bldingDict['buildingShape']=self.building['buildingShape']
		bldingDict['wallConstruction']=self.building['wallConstruction']
		bldingDict['WWR']=self.building['WWR']
		bldingDict['peoplePerArea']=self.building['peoplePerArea']
		return bldingDict


	