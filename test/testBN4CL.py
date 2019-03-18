

#define the building
import numpy as np 
from IntelligentBuildingPerformanceDesign.AIBPD.data.database import Database
from IntelligentBuildingPerformanceDesign.AIBPD.data.building import Building
from IntelligentBuildingPerformanceDesign.AIBPD.data.preprocessing import PreprocessingCBECS
from IntelligentBuildingPerformanceDesign.AIBPD.algorithms.similarityAnalysis import Similarity
from IntelligentBuildingPerformanceDesign.AIBPD.algorithms.BN4CL2 import BN4CL
#select database. enbodded data base including CBECS2012.
database=Database()
CBECS2012DF=database.select('CBECS2012')
similar=Similarity()
preprocess=PreprocessingCBECS()
BN_model=BN4CL()

proposedBuilding=Building()
#define key attributes for the buildings.
proposedBuildingDict={'climateZone':5,   'principleActivity':3,
					'buildingArea': 130000, 'yearOfConstruction':1990,
					'buildingShape':2,      'wallConstruction':2,
					'WWR': 2,             'numPeople': 6,   'CDD65':2400}
proposedBuilding.defineBuilding(proposedBuildingDict)

CBECS2012DF=CBECS2012DF[CBECS2012DF['CDD65']>500]
CBECS2012DF=preprocess.forHECLClf(CBECS2012DF)
CBECS2012DF=CBECS2012DF.dropna()
#similarBuildingDF=CBECS2012DF[CBECS2012DF['HECS']==1.0]
similarBuildingDF=similar.kSimilarBuildings(proposedBuilding,CBECS2012DF,300)
similarBuildingDF=similarBuildingDF.dropna()
BN_model.fit(similarBuildingDF)
BN_model.predict(proposedBuilding)