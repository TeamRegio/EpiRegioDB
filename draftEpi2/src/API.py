import os
import sys
from django.conf import settings
import pymysql
#sys.path.insert(1, r'website/')#tell python the path of the project

from draftEpi2 import setup #setup function defined in __init__.py of the project (here website)
setup()

from django.db import models
from table_manager.models import *



#test functions
# #TODO: write proper unitests
def __main__():
#
# # 	print("API functions")
# # 	print("Is the database accessible?")
# #
# 	REM = REMAnnotation.objects.filter(REMID = "REM0000001").values('REMID__CREMID')
# 	print(REM)
# #
# # 	print("all REMs of a gene")
# # 	REMs = REMAnnotation.objects.filter(geneID = 'ENSG00000139874')
# # 	for i in REMs:
# # 		print(i)
# #
# # 	print("sampleInfo")
# # 	sample = sampleInfo.objects.get(sampleID = 'R_ENCBS336CDQ')
# # 	print(sample)
# #
# # This is not working because of the missing primary key, which is geneExpressionID in the database ->same for REMActivity TODO: rausfinden wie man combined primary key angibt in mysql
# 	print("geneExpression")
# 	# geneExp = geneExpression.objects.filter(sampleID='R_ENCBS336CDQ')[:1].values('sampleID__cellTypeID__cellTypeName')
# 	geneExp = geneExpression.objects.filter(sampleID='R_ENCBS336CDQ')[:1]
# 	# print(geneExpression.objects.filter(sampleID='R_ENCBS336CDQ')[:1].values('expressionLog2TPM'))
# 	print(geneExp)
# # #
# # 	print("genomeAnnotation")
# # 	genome = genomeAnnotation.objects.all()
# # 	print(genome)
# #
# # 	print("celltypes")
# # 	cellType = cellTypes.objects.get(cellTypeID = 'CTID_0000001')
# # 	print(cellType)
# #
# # 	print("geneAnnotation")
# # 	geneAnno = geneAnnotation.objects.get(geneID = 'ENSG00000223972')
# # 	print(geneAnno)
#
	# print("CREM")
	# crem = CREMAnnotation.objects.filter(REMID = 'REM0000001')
	# print(crem)
#
	# print("REMActivity")
	# REMActiv = REMActivity.objects.filter(REMID = 'REM0000001')[:3].values('sampleID__cellTypeID__cellTypeName')
	# print(REMActiv)
#
#


	REMID_list = ['REM0000001', 'REM0000002', 'REM0000003']
	cellTypes_list = ['pancreas', 'macrophage']
	REMID = 'REM0000001'


	for cellType in cellTypes_list:
		activity = REMActivity.objects.filter(REMID=REMID).filter(sampleID__cellTypeID__cellTypeName=cellType).values()
		print(cellType)
		print(activity)
# for pancrease(CTID_0000064) should be equivalent to
# SELECT * FROM REMActivity WHERE REMID='REM0000001' AND sampleID IN
# (SELECT sampleID FROM sampleInfo WHERE cellTypeID='CTID_0000064');


if __name__ == "__main__":
	__main__()


def API_CellTypesActivity(REM, cellTypes_list):
	REMID = REM['REMID']
	# matching_samples = []
	# for line in matching_REMs:
	# 	if [sampleInfo.objects.get(sampleID=line['sampleID']).values('cellTypeID__cellTypeName')] in cellTypes_list:
	# 		matching_samples.append(line)

	for cellType in cellTypes_list:
		activity = REMActivity.objects.filter(REMID=REMID).filter(sampleID__cellTypeID__cellTypeName=cellType).values('dnase1Log2')
	print(activity)

	return REM




def API_REMID(REMID_list, cellTypes_list):

	hit_list = []
	for i in REMID_list:

		dataset = REMAnnotation.objects.filter(REMID=i).values()  # .values hands back a queryset containing dictionaries
		this_rem = dataset[0]  # we get back a queryset, with [0] we get it into a dictionary

		# get the additional columns for the CREMS
		CREMInfo = CREMAnnotation.objects.filter(REMID=i).values()

		# if there are cellTypes that should be filtered for, we do it here for every single REM, to directly add it
		# to the REMs dictionary
		if len(cellTypes_list) > 0:
			this_rem = API_CellTypesActivity(this_rem, cellTypes_list)

		this_rem['REMsPerCREM'] = CREMInfo[0]['REMsPerCREM']  # append the attributes
		this_rem['CREMID'] = CREMInfo[0]['CREMID']


		hit_list.append(this_rem)


	return hit_list  # our list of objects, fitting the query_list


# for n, single_obj in enumerate(data_set):  # we get back a queryset that we write into a list of objects
# 	print(single_obj)
# 	single_obj['REMsPerCREM'] = CREMInfo[n]['REMsPerCREM']  # append the attributes
# 	single_obj['CREMID'] = CREMInfo[n]['CREMID']
# 	hit_list.append(single_obj)