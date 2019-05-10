'''
convert class is used to convert idf.json to BPID a csv file.
'''
import json
import csv
import idf # this module designed for parsing structured idf to csv file.
import re
from aibpd.data.building import Building
class convert(idfJsonFile);

	def __init__(self,**kwargs):
		return true
	
	
	def convertJSONPhase1(idfJsonFile):
	'''
	
	'''
		with open(idfJsonFile) as idfjson:
			idfjson = json.loads(idfjson)
			f = csv.writer(open("test.csv", "wb+"))
			# Write CSV Header, If you dont need that, remove this line
			f.writerow(["pk", "model", "codename", "name", "content_type"])
			for row in idfjson:
				f.writerow([x["pk"],x["model"],x["fields"]["codename"],x["fields"]["name"],x["fields"]["content_type"]])
	def readIDFtoDict(idfFile):
	'''
	read data from 
	'''
		idf_dict = {}
		items=[]
		insideIndex=True
		with open(idfile) as idf:
			for line in idf:
				if re.search('(\w+),$',line):
					className=re.search('(\w+),$',line).group(0)
					items=[]
					insideIndex=True
				elif re.search('(.+),\s+!-(.+)',line) and insideIndex:
					itemName=re.search('(.+),\s+!-(.+)',line).group(2)
					itemValue=re.search('(.+),\s+!-(.+)',line).group(1)
					items.append({itemName:itemValue})
				elif re.search('(.+);\s+!-(.+)',line) and insideIndex:
					itemName=re.search('(.+);\s+!-(.+)',line).group(2)
					itemValue=re.search('(.+);\s+!-(.+)',line).group(1)
					items.append({itemName:itemValue})
					insideIndex = False
					idf_dict[className]=items
		return idf_dict

if __name__ == '__main__':
	from IntelligentBuildingPerformanceDesign.__init__ import currentUrl
	idf_file_path=currentUrl+"\\resources\\5ZoneAutoDXVAV.idf"

	convertIDF = convert()
	one_building = convertIDF.readIDF()