

#define the building

from IntelligentBuildingPerformanceDesign.AIBPD.data.database import Database
from IntelligentBuildingPerformanceDesign.AIBPD.data.building import Building
from IntelligentBuildingPerformanceDesign.AIBPD.algorithms.similarityAnalysis import Similarity
from IntelligentBuildingPerformanceDesign.AIBPD.algorithms.BN4CL import BN4CL
#select database. enbodded data base including CBECS2012.
database=Database()
CBECS2012DF=database.select('CBECS2012')

proposedBuilding=Building()
proposedBuildingDict={'climateZone':1,   'principleActivity':1,
					'buildingArea': 100000, 'yearOfConstruction':1930,
					'buildingShape':2,      'wallConstruction':2,
					'WWR': 2,             'numPeople': 6,
					'COOLLOAD':11,'CDD65':1,'COOLP':1}
proposedBuilding.defineBuilding(proposedBuildingDict)

#get the attributes used to calculate similarity
similarity=Similarity()
similarBuildingsDF=similarity.kSimilarBuildings(proposedBuilding,CBECS2012DF,300)
print(similarBuildingsDF)
#Use Bayesian Network Classifier to select cooling system for the proposed building.
BN4CLSection=BN4CL()
BN4CLSection.fit(similarBuildingsDF)
BN4CLSection.predict(proposedBuilding)