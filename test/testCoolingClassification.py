from IntelligentBuildingPerformanceDesign.AIBPD.data.preprocessing import PreprocessingCBECS
from IntelligentBuildingPerformanceDesign.AIBPD.data.database import Database
import numpy as np
import pandas as pd

database=Database()
CBECS_DF=database.select('CBECS2012')
Preproc=PreprocessingCBECS()
CBECS_DF=CBECS_DF[CBECS_DF['CDD65']>=500][CBECS_DF['principleActivity']>=2][CBECS_DF['principleActivity']<3]
CBECS_DF=Preproc.forCoolingClf(CBECS_DF)
