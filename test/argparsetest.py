from aibpd.data.database import Database
from aibpd.data.preprocessing import PreprocessingCBECS
import numpy as np
import pandas as pd
import aibpd
database=Database(file_path='CBECS2012.csv')
Preproc=PreprocessingCBECS(database)
building=database.find_building_by_ID(1)
#print(building)
#aibpd.summary(CBECS_DF,building)
feature_weights={'climateZone':5,
			'principleActivity':5,
			'buildingAreaCategory': 10,
			'yrConstructionCategory':8}
similar_buildings_DB=aibpd.get_ksimilar(database,building,50,feature_weights)
aibpd.summary(similar_buildings_DB,building)