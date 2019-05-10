from aibpd.data.preprocessing import PreprocessingCBECS
from aibpd.data.database import Database
import numpy as np
import pandas as pd

database=Database()
CBECS_DF=database.select()
