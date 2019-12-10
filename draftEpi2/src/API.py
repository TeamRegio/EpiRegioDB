import os
import sys
from django.conf import settings
# import pymysql
#sys.path.insert(1, r'website/')#tell python the path of the project

from draftEpi2 import setup #setup function defined in __init__.py of the project (here website)
setup()

from django.db import models
from table_manager.models import *



#test functions
# #TODO: write proper unitests
# def __main__():
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




# if __name__ == "__main__":
# 	__main__()


"""
All query functions do a first filter step to give back the fitting data. Next the functions to filter
for cellTypes (if any cellTypes given) and for adding the CREM information are called. The additional information is
added to the dictionaries.
"""



# For every query, we give the possibility to give back the activity of the REMs. This function is only
# called, when there are cellTypes given. Another option is to provide a threshold, which excludes all the REMs that
# have an activity below it. For more than one cellType a REM's activity has to exceed in ALL of them.
# If no threshold was set, the view returns a 0 as threshold.
def API_CellTypesActivity(REM, cellTypes_list=[], activ_thresh=0.0):

	REMID = REM['REMID']
	for cellType in cellTypes_list:
		matching_samples = REMActivity.objects.filter(REMID=REMID).filter(sampleID__cellTypeID__cellTypeName=cellType).filter(dnase1Log2__gte=activ_thresh).values()
		activity = 0
		if len(matching_samples) > 0:  # as it's possible that no REM is remaining
			for sample in matching_samples:
				activity += sample['dnase1Log2']
			mean_activity = activity/len(matching_samples)
			REM[cellType + '_dnase1Log2'] = mean_activity
			REM[cellType + '_samplecount'] = len(matching_samples)
		else:
			return  # we return None if there is no match. The Nones are filtered out in the origin function
	return REM


# Giving back the additional information about the CREM that the REMs are belonging to
def API_CREM(REM):

	# get the additional columns for the CREMS
	CREMInfo = CREMAnnotation.objects.filter(REMID=REM['REMID']).values()
	REM['REMsPerCREM'] = CREMInfo[0]['REMsPerCREM']  # append the attributes
	REM['CREMID'] = CREMInfo[0]['CREMID']

	return REM


# This is only for the detail view when clicking on a CREM-link
def API_CREM_overview(CREMID):

	dataset = list(CREMAnnotation.objects.filter(CREMID=CREMID).values(
		'REMID_id', 'CREMID', 'chr', 'start', 'end', 'REMsPerCREM', 'version', 'REMID_id__geneID', 'REMID_id__start',
		'REMID_id__end', 'REMID_id__regressionCoefficient', 'REMID_id__pValue'))

	return dataset


# The REMID query. Every REM is handled separately.
def API_REMID(REMID_list, cellTypes_list=[], activ_thresh=0.0):

	hit_list = []
	for i in REMID_list:

		dataset = REMAnnotation.objects.filter(REMID=i).values()  # .values hands back a queryset containing dictionaries
		this_rem = dataset[0]  # we get back a queryset, with [0] we get it into a dictionary

		# get the additional columns for the CREMS
		this_rem = API_CREM(this_rem)

		# if there are cellTypes that should be filtered for, we do it here for every single REM, to directly add it
		# to the REMs dictionary
		if len(cellTypes_list) > 0:
				this_rem = API_CellTypesActivity(this_rem, cellTypes_list, activ_thresh)

		hit_list.append(this_rem)
		hit_list = [x for x in hit_list if x is not None]  # if a REM's activity in a cell type is under the threshold,
		# we returned None into the list, now we get rid of it

	return hit_list  # our list of objects, fitting the query_list


# If a user provides the geneSymbols, we convert them into ENSG format and use the other functions
def API_SymbolToENSG(symbol_list):

	hit_list = []
	for symbol in symbol_list:

		dataset = geneAnnotation.objects.get(geneSymbol=symbol)
		this_ID = dataset.geneID

		hit_list.append(this_ID)

	return hit_list  # our list of objects, fitting the query_list


# For the GeneID query: given a set of genes, we look up all the REMs for each of them and add
# the additional information
def API_ENSGID(gene_list, cellTypes_list=[], activ_thresh=0.0):

	hit_list = []

	for i in gene_list:
		dataset = list(REMAnnotation.objects.filter(geneID=i).values())  # we convert the queryset into a list so we can
		# add values to it
		for n in range(len(dataset)):
			dataset[n] = API_CREM(dataset[n])
			if len(cellTypes_list) > 0:
				dataset[n] = API_CellTypesActivity(dataset[n], cellTypes_list, activ_thresh)

		hit_list = hit_list + dataset
		hit_list = [x for x in hit_list if x is not None]  # if a REM's activity in a cell type is under the threshold,
		# we returned None into the list, now we get rid of it

	return hit_list


# Is supposed to be used to display the information we have about a gene
def API_ENSGID_geneInfo(gene_list):

	hit_list = []
	for gene in gene_list:
		dataset = geneAnnotation.objects.filter(geneID=gene).values()
		hit_list.append(dataset)

	return hit_list


# For the GeneRegion query: find all the REMs located in the given regions
def API_Region(region_list, cellTypes_list=[], activ_tresh=0.0):

	hit_list = []

	for i in region_list:
		dataset = list(REMAnnotation.objects.filter(chr=i[0]).filter(start__gte=i[1]).filter(end__lte=i[2]).values())

		for n in range(len(dataset)):
			dataset[n] = API_CREM(dataset[n])
			if len(cellTypes_list) > 0:
				dataset[n] = API_CellTypesActivity(dataset[n], cellTypes_list, activ_tresh)

		hit_list = hit_list + dataset
		hit_list = [x for x in hit_list if x is not None]  # if a REM's activity in a cell type is under the threshold,
		# we returned None into the list, now we get rid of it

	return hit_list  # our list of dictionaries, fitting the query_list
