'''
Test the similarityEuclidian class
'''
from AIBPD.DDBPD.data.preprocessing import PreprocessingCBECS
from AIBPD.DDBPD.data.database import Database
import numpy as np
import pandas as pd
from AIBPD.DDBPD.data.building import Building
from AIBPD.DDBPD.algorithms.similarity import SimilarityEuclidian
database=Database()
CBECS_DF=database.select('CBECS2012')
Preproc=PreprocessingCBECS()

CBECS_DF['CDD65'].hist(bins=100)
CBECS_DF=CBECS_DF[CBECS_DF['CDD65']>=500][CBECS_DF['principleActivity']>=2][CBECS_DF['principleActivity']<3]
CBECS_DF=Preproc.forCoolingClf(CBECS_DF)

proposedBuilding=Building()

proposedBuildingDict={'climateZone':5,   'principleActivity':3,
					'buildingArea': 72000, 'yearOfConstruction':1990,
					'buildingShape':2,      'wallConstruction':2,
					'WWR': 2,             'numPeople': 6,   'CDD65':2400}
proposedBuilding.defineBuilding(proposedBuildingDict)
similar=SimilarityEuclidian()
similarbuildings=SimilarityEuclidian.get(proposedBuilding,CBECS_DF,k=50)
print(similarbuildings)
