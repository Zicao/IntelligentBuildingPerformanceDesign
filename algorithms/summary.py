'''
Generate a standard summary report for the design building. This summary report should contain following information:
    *Total energy consumption; Total source energy consumption, 
    *End uses;
    *Energy performance ranking.
    *...
'''
from aibpd.algorithms import Similarity
import numpy as np
class BaseSummary():
    '''
    conduct several basic statistical analysis.
    Arg:
        building, the design building.
        dataDF, the dataset.
    '''
    
    def __init__(self, datasetDF):
        '''
        
        '''

    def loadData(self,datasetDF):
        '''
        load the dataset
        '''
        pass
    def categoricalorNumeric(self,datasetDF):
        """
        sort out categorical features and numeric features
        
        parameters:
        ---------------
        datasetDF: a DataFrame object that contains the dataset.

        Return:
        ----------

        Example:
        ----------

        """
        pass

    def statisticalContinuous(self,datasetDF,featurelist=continuousFeatureList):
        '''
        generate some common statistical analysis for the continuous variables.

        parameters:
        ----------
        datasetDF: a DataFrame object that contains the dataset.

        return: DataFrame.describe() function.

        '''
        return datasetDF[featurelist].describe()


    def statisticalCategorical(self,datasetDF,featurelist=categoricalFeatureList):
        '''
        generate some common statistical analysis for the categorical variables.

        parameters:
        -----------
        datasetDF: a DataFrame object that contains the dataset.
        '''
        return datasetDF[featurelist].hist()


    def rankingEUI(self):
        '''
        Rank buildings 
        '''
        pass

class Summary():

    '''use to generate a summary report for a design building.

    Parameters:
    ----------
    building, the design building, a Building Object, 
    dataset, the dataset used to generate the report.

    Return:
    ----------

    '''
    def __init__(self, building, datasetDF):
        self.building=building
        self.datasetDF=datasetDF

    def standardReport(self,building,):
        '''generate a standard report in a csv file. 1) ranking based
            on building performance EUI etc.
        Parameters:
        ----------

        Return:
        ----------
        
        '''
        # rank based on EUI
        n=np.searchsorted(self.datasetDF['EUI'].values,self.building)





class DatasetSummary():
    '''
    to generate a summary report for the dataset.
    '''
    def __init__(self,datasetDF,reportType='csv'):
        pass

    def standardReport(self):
        pass 




if __name__ == '__main__':
    print('good')