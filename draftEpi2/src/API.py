import os, sys, math
from django.conf import settings
#import pymysql
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

# Function to add the modelScore to the dictionary, taking a list of dictionaries
def API_modelScore(hit_list):

	for hit in range(len(hit_list)):
		try:
			hit_list[hit]['modelScore'] = -math.log2(hit_list[hit]['pValue'])
		except KeyError:
			hit_list[hit] = None

	hit_list = [x for x in hit_list if x is not None]  # if a REM's activity in a cell type is under the threshold,

	return hit_list

# For every query, we give the possibility to give back the activity of the REMs. This function is only
# called, when there are cellTypes given. Another option is to provide a threshold, which excludes all the REMs that
# have an activity below it. For more than one cellType a REM's activity has to exceed in ALL of them.
# If no threshold was set, the view returns a 0 as threshold.
def API_CellTypesActivity(REM, cellTypes_list=[], activ_thresh=0.0):

	try:
		REMID = REM['REMID']
	except KeyError:
		return None

	try:
		activ_thresh = float(activ_thresh)
	except ValueError:
		activ_thresh = 0

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
			return None  # we return None if there is no match. The Nones are filtered out in the origin function
	return REM


# Given a list of cellTypes, this function checks whether there are samples in the database that match these cellTypes\
# It uses contains as filter, as the original use is to give suggestions for characters the user enters
def API_cellTypesValidation(cellTypes_list=[]):

	cellType_valid = []
	for cellType in cellTypes_list:
		matching_samples = sampleInfo.objects.filter(cellTypeID__cellTypeName__contains=str(cellType).lower()).values_list(
			'cellTypeID', 'cellTypeID__cellTypeName', flat=False)

		for i in matching_samples:  # get rid of double entries
			if i not in cellType_valid:
				cellType_valid.append(i)

	return cellType_valid


# To look up for the gene Symbol, whether we have REMs available for them. If not, we won't display that as an option
# in the gene symbol input field
def API_geneSymbolValidation(geneSymbol_list=[]):

	geneSymbol_valid = []
	for symbol in geneSymbol_list:
		matching_samples = REMAnnotation.objects.filter(geneID_id__geneSymbol__contains=symbol.upper()).values_list(
			'geneID_id__geneSymbol', flat=False)

		for i in matching_samples:  # get rid of double entries
			if i not in geneSymbol_valid:
				geneSymbol_valid.append(i)

	return geneSymbol_valid


# Giving back the additional information about the CREM that the REMs are belonging to
def API_CREM(REM):

	try:
		REMID = REM['REMID']
	except KeyError:
		return None
	# get the additional columns for the CREMS
	CREMInfo = CREMAnnotation.objects.filter(REMID=REMID).values()
	try:
		REM['REMsPerCREM'] = CREMInfo[0]['REMsPerCREM']  # append the attributes
		REM['CREMID'] = CREMInfo[0]['CREMID']
	except IndexError:
		return None

	return REM


# This is only for the detail view when clicking on a CREM-link
def API_CREM_overview(CREMID_list):

	hit_list = []
	for crem in CREMID_list:
		try:
			dataset = list(CREMAnnotation.objects.filter(CREMID=crem).values(
				'REMID_id', 'CREMID', 'chr', 'start', 'end', 'REMsPerCREM', 'version', 'REMID_id__geneID', 'REMID_id__start',
				'REMID_id__end', 'REMID_id__regressionCoefficient', 'REMID_id__pValue'))
		except KeyError:
			continue

		# We don't use the other function, as the dictionary entry has  a different name for the CREMs
		for n in range(len(dataset)):
			try:
				dataset[n]['modelScore'] = -math.log2(dataset[n]['REMID_id__pValue'])
			except KeyError:
				dataset[n] = None
			hit_list = hit_list + dataset

		hit_list = [x for x in hit_list if x is not None]  # if a REM's activity in a cell type is under the threshold,

		return hit_list


# given a sample_id the function return the correpsonding cell_name
def  API_celltypeID_celltype(sample_id):

	try:
		cellType_id = sampleInfo.objects.filter(sampleID=sample_id).values()[0]
	except IndexError:
		return None

	cellName = cellTypes.objects.filter(cellTypeID=cellType_id['cellTypeID_id']).values()[0]

	return(cellName['cellTypeName'])


# determines for a given REM_ID the tissue/celltype activity for all samples
# return the rem_id with the new field cellTypeActivity which is a dictionary {CellName : dnase1Log2}
def API_cellType_activity_per_REM(rem_id):

	# get the celltype activity
	try:
		matching_samples = REMActivity.objects.filter(REMID=rem_id['REMID']).values()
	except KeyError:
		return None
	activity = {}
	for elem in matching_samples:

		cellType_name = API_celltypeID_celltype(elem['sampleID_id']) #determines the cellType name from the sampleID 
		if cellType_name in activity.keys(): #take care of tisue or celltypes that occur more than once
			activity[cellType_name] = (float(activity[cellType_name]) + float(elem['dnase1Log2']))/2			
		else:
			activity[cellType_name] = elem['dnase1Log2']

		rem_id['cellTypeActivity'] = activity
		rem_id['geneSymbol'] = geneAnnotation.objects.filter(geneID = rem_id['geneID_id']).values('geneSymbol')[0]['geneSymbol'] # QuerySet 
	return rem_id

# The REMID query for the REST_API, also outputs the activity of all celltypes per REM. Every REM is handled separately.
# output fields: chr, start, end, geneID_id, REMID, regressionCoefficient, pValue, version, REMsPerCREM, CREMID, cellTypeActivity -> dictionary of all cell types
def API_REMID_celltype_activity(REMID_list):

	helper = API_REMID(REMID_list) #worst case this an empty list
	hit_list = []
	for i in helper:
		hit_list.append(API_cellType_activity_per_REM(i))
	return hit_list


# The REMID query. Every REM is handled separately.
def API_REMID(REMID_list, cellTypes_list=[], activ_thresh=0.0):

	hit_list = []
	for i in REMID_list:

		dataset = REMAnnotation.objects.filter(REMID=i).values()  # .values hands back a queryset containing dictionaries
		try:
			this_rem = dataset[0]  # we get back a queryset, with [0] we get it into a dictionary
		except IndexError:
			return 'Error - Invalid REMID: '+i  # if there is a REMID that is not in the DB we display it as an error

		# get the additional columns for the CREMS
		this_rem = API_CREM(this_rem)
		this_rem['geneSymbol'] = geneAnnotation.objects.get(geneID=this_rem['geneID_id']).geneSymbol

		# if there are cellTypes that should be filtered for, we do it here for every single REM, to directly add it
		# to the REMs dictionary
		if len(cellTypes_list) > 0:
				this_rem = API_CellTypesActivity(this_rem, cellTypes_list, activ_thresh)

		hit_list.append(this_rem)

	hit_list = [x for x in hit_list if x is not None]  # if a REM's activity in a cell type is under the threshold,
	# we returned None into the list, now we get rid of it

	hit_list = API_modelScore(hit_list)

	return hit_list  # our list of objects, fitting the query_list


# If a user provides the geneSymbols, we convert them into ENSG format and use the other functions
def API_SymbolToENSG(symbol_list):

	hit_list = []
	for symbol in symbol_list:
		try:
			this_ID = geneAnnotation.objects.get(geneSymbol=symbol).geneID
		except IndexError:
			return 'Error - Invalid gene symbol: '+symbol  # display the error when there is no matching geneSymbol

		hit_list.append(this_ID)

	return hit_list  # our list of objects, fitting the query_list


# The GeneID query for the REST_API, also outputs the activity of all celltypes per REM. Every REM is handled separately.
# output fields: chr, start, end, geneID_id, REMID, regressionCoefficient, pValue, version, REMsPerCREM, CREMID, cellTypeActivity -> dictionary of all cell types
def API_GeneID_celltype_activity(REMID_list):

	helper = API_ENSGID(REMID_list) #determine REMs for the given GeneIDs
	hit_list = []
	for i in helper:
		hit_list.append(API_cellType_activity_per_REM(i)) # determine activity
	return hit_list


# For the GeneID query: given a set of genes, we look up all the REMs for each of them and add
# the additional information
def API_ENSGID(gene_list, cellTypes_list=[], activ_thresh=0.0, gene_format='id_format'):

	hit_list = []
	no_hit = []
	for i in gene_list:
		dataset = list(REMAnnotation.objects.filter(geneID=i).values())  # we convert the queryset into a list so we can
		if not dataset:  # if it's empty we have no fitting geneID
			if not list(geneAnnotation.objects.filter(geneID=i).values()):  # if this id is not existent at all
				return 'Error - Invalid gene ID. This is not an ID that is contained in the hg38 genome: '+i, no_hit
			else:
				no_hit.append(i)

		# add values to it
		for n in range(len(dataset)):

			dataset[n] = API_CREM(dataset[n])
			dataset[n]['geneSymbol'] = geneAnnotation.objects.get(geneID=dataset[n]['geneID_id']).geneSymbol

			if len(cellTypes_list) > 0:
				dataset[n] = API_CellTypesActivity(dataset[n], cellTypes_list, activ_thresh)

		hit_list = hit_list + dataset

	hit_list = [x for x in hit_list if x is not None]  # if a REM's activity in a cell type is under the threshold,
	# we returned None into the list, now we get rid of it

	hit_list = API_modelScore(hit_list)

	if gene_format == 'symbol_format':  # if there are no REMs for a gene and the use filtered for symbols,
		# we also show the symbols
		for i in range(len(no_hit)):
			no_hit[i] = geneAnnotation.objects.get(geneID=no_hit[i]).geneSymbol

	return hit_list, no_hit


# Is supposed to be used to display the information we have about a gene
# output fields: chr, start, end, geneID, geneSymbol, alternativeGeneID, isTF, strand, annotationVersion_id
def API_ENSGID_geneInfo(gene_list):

	hit_list = []
	for gene in gene_list:
		try:
			dataset = geneAnnotation.objects.filter(geneID=gene).values()[0]
		except IndexError:
			continue

		hit_list.append(dataset)

	return hit_list


# The Region query for the REST_API, also outputs the activity of all celltypes per REM. Every REM is handled separately.
# region_list format: [[chr, start, end], [chr, start, end]]
def API_Region_celltype_activity(region_list):

	helper = API_Region(region_list)
	hit_list = []
	for i in helper:
		hit_list.append(API_cellType_activity_per_REM(i))
	return hit_list


# For the GeneRegion query: find all the REMs located in the given regions
def API_Region(region_list, cellTypes_list=[], activ_tresh=0.0):

	hit_list = []
	for i in region_list:
		try:
			dataset = list(
				REMAnnotation.objects.filter(chr=i[0]).filter(start__gte=i[1]).filter(end__lte=i[2]).values())

			for n in range(len(dataset)):
				dataset[n] = API_CREM(dataset[n])
				dataset[n]['geneSymbol'] = geneAnnotation.objects.get(geneID=dataset[n]['geneID_id']).geneSymbol

				if len(cellTypes_list) > 0:
					dataset[n] = API_CellTypesActivity(dataset[n], cellTypes_list, activ_tresh)

		except KeyError:
			continue

		hit_list = hit_list + dataset

	hit_list = [x for x in hit_list if x is not None]  # if a REM's activity in a cell type is under the threshold,
	# we returned None into the list, now we get rid of it

	hit_list = API_modelScore(hit_list)

	return hit_list  # our list of dictionaries, fitting the query_list

