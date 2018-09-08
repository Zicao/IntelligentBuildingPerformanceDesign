

#define the building

from IntelligentBuildingPerformanceDesign.AIBPD.data.database import Database
from IntelligentBuildingPerformanceDesign.AIBPD.data.building import Building
from IntelligentBuildingPerformanceDesign.AIBPD.algorithms.similarityAnalysis import Similarity
from IntelligentBuildingPerformanceDesign.AIBPD.algorithms.BN4CL import BN4CL
#select database. enbodded data base including CBECS2012.
database=Database()
CBECS2012DF=database.select('CBECS2012')

proposedBuilding=Building()
#define key attributes for the buildings.
proposedBuildingDict={'climateZone':1,   'principleActivity':1,
					'buildingArea': 100000, 'yearOfConstruction':1930,
					'buildingShape':2,      'wallConstruction':2,
					'WWR': 2,             'numPeople': 6,
					'COOLLOAD':11,'CDD65':1,'COOLP':0}
proposedBuilding.defineBuilding(proposedBuildingDict)
#get similar buildings from database (CBECS2012 database)
similarBuildingDF=Similarity.kSimilarBuildings(proposedBuilding,CBECS2012DF)
#train the model
BN4CL.fit(similarBuildingDF)
#predict the optimal cooling system for the proposedBuilding.
BN4CL.predict(proposedBuilding)
''''''