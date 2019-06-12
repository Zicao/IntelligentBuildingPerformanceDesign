from aibpd.data.database import Database
from aibpd.data.preprocessing import PreprocessingCBECS
import numpy as np
import pandas as pd
import aibpd
database=Database(file_path='CBECS2012.csv')
Preproc=PreprocessingCBECS(database)
print(database.dataDF['MAINCL'])