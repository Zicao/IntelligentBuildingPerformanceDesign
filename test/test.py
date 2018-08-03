

#define the building
#

from IntelligentBuildingPerformanceDesign.AIBPD.data.database import Database
from IntelligentBuildingPerformanceDesign.AIBPD.data.building import Building
from IntelligentBuildingPerformanceDesign.AIBPD.algorithms.similarityAnalysis import Similarity
from IntelligentBuildingPerformanceDesign.AIBPD.algorithms.BN4CL import BN4CL
#select database. enbodded data base including CBECS2012.
database=Database()
CBECS2012DF=database.select('CBECS2012')

proposedBuilding=Building()
proposedBuildingDict={'climateZone':3,   'principleActivity':2,
					'buildingArea': 100000, 'yearOfConstruction':1930,
					'buildingShape':2,      'wallConstruction':2,
					'WWR': 2,             'numPeople': 6}
proposedBuilding.defineBuilding(proposedBuildingDict)

#get the attributes used to calculate similarity
prpsedBlding4SmlarAnalysis=proposedBuilding.blding4SimilarityAnalysis()
similarity=Similarity()
similarBuildingsDF=similarity.kSimilarBuildings(prpsedBlding4SmlarAnalysis,CBECS2012DF,300)
BN4CLSection=BN4CL()
BN4CLSection.fit(similarBuildingsDF)