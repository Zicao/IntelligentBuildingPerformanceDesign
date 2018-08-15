

#define the building

from IntelligentBuildingPerformanceDesign.AIBPD.data.database import Database
from IntelligentBuildingPerformanceDesign.AIBPD.data.building import Building
from IntelligentBuildingPerformanceDesign.AIBPD.algorithms.similarityAnalysis import Similarity
from IntelligentBuildingPerformanceDesign.AIBPD.algorithms.BN4CL import BN4CL
#select database. enbodded data base including CBECS2012.
database=Database()
BEEMRDF=database.select('BEEMR')

proposedBuilding=Building()
proposedBuildingDict={'climateZone':1,   'principleActivity':1,
					'buildingArea': 100000, 'yearOfConstruction':1930,
					'buildingShape':2,      'wallConstruction':2,
					'WWR': 2,             'numPeople': 6,
					'COOLLOAD':11,'CDD65':1,'COOLP':0}
proposedBuilding.defineBuilding(proposedBuildingDict)
print(BEEMRDF)
''''''