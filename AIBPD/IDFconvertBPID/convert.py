'''
convert class is used to convert idf.json to BPID a csv file.
'''
import json
import csv
import idf # this module designed for parsing structured idf to csv file.

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
	def convertIDFPhase1(idfFile):
	'''
	
	'''
		with open(idfFile) as idf:
			idf = idf.
