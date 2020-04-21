# import pymysql

import os, sys, math
from django.conf import settings
import numpy as np
from pybedtools import BedTool


#sys.path.insert(1, r'website/')#tell python the path of the project

from draftEpi2 import setup #setup function defined in __init__.py of the project (here website)
setup()

from django.db import models
from table_manager.models import *
from django.core.exceptions import ObjectDoesNotExist

#test functions
# def __main__():


# if __name__ == "__main__":
# 	__main__()

"""
All query functions do a first filter step to give back the fitting data. Next the functions to filter
for cellTypes (if any cellTypes given) and for adding the CREM information are called. The additional information is
added to the dictionaries.
"""


# Function to get the link to the gProfiler analysis with the genes that are associated to the REMs in the query result.
def gProfiler_link(data):

	try:
		entry = [x for x in list(data[0].keys()) if x.startswith('geneID') or x.endswith('geneID')][0]
		gene_list = list(set([x[entry] for x in data]))
		gene_string = '%0A'.join(gene_list[:90])
		# print(gene_string)
		link = "https://biit.cs.ut.ee/gprofiler/gost?organism=hsapiens&query=" + gene_string + "&ordered=false&all_results=false&no_iea=false&combined=false&measure_underrepresentation=false&domain_scope=annotated&significance_threshold_method=g_SCS&user_threshold=0.05&numeric_namespace=ENTREZGENE_ACC&sources=GO:MF,GO:CC,GO:BP,KEGG,TF,REAC,MIRNA,HPA,CORUM,HP,WP&background="
		return link, len(gene_list)
	except IndexError:
		return None, None


# def recreation_link(request):
#
# 	post_data = {'gene_format': 'numeric', 'geneID_numeric':'ENSG00000139874, ENSG00000274220'}
# 	response = request.get('http://127.0.0.1:8000/geneQuery/', data=post_data)


# As we normalized the modelScore and added it as column to the REMAnnotation table, we don't need this function anymore
# Function to add the modelScore to the dictionary, taking a list of dictionaries
# def API_modelScore(hit_list):
#
# 	for hit in range(len(hit_list)):
# 		try:
# 			hit_list[hit]['modelScore'] = -math.log2(hit_list[hit]['pValue'])
# 		except KeyError:
# 			hit_list[hit] = None
#
# 	hit_list = [x for x in hit_list if x is not None]  # if a REM's activity in a cell type is under the threshold,
#
# 	return hit_list


# For every query, we give the possibility to give back the activity of the REMs. This function is only
# called, when there are cellTypes given. Another option is to provide a threshold, which excludes all the REMs that
# have an activity below it. For more than one cellType a REM's activity has to exceed in ALL of them.
# If no threshold was set, the view returns a 0 as threshold.
def API_CellTypesActivity(REM, cellTypes_list=[], score_thresh=['no', -1,1], activ_thresh=0.0):

	try:
		REMID = REM['REMID']
	except KeyError:
		return None

	try:
		activ_thresh = float(activ_thresh)
	except ValueError:
		activ_thresh = 0.0

	for cellType in cellTypes_list:
		matching_samples = REMActivity.objects.filter(REMID=REMID).filter(sampleID__cellTypeID__cellTypeName=cellType).values()
		activity = 0
		score = 0

		if len(matching_samples) > 0:  # as it's possible that no REM is remaining
			for sample in matching_samples:
				activity += sample['dnase1Log2']
				score += sample['standDnase1Log2']
			mean_activity = activity/len(matching_samples)
			mean_score = score/len(matching_samples)

			if score_thresh != ['no', -1, 1] or activ_thresh != 0.0:  # we only need to check with additional filters if
				# thresholds were set
				if score_thresh[0] == 'abs':
					if abs(score_thresh[1]) <= abs(mean_score) <= abs(score_thresh[2]) and mean_activity >= activ_thresh:
						# only if the mean score and activity exceeds the  threshold in ALL of the cell types, the REM is
						# returned. If it doesn't exceed the thresh in one cell type, we return None and thus remove it from
						# the output
						REM[cellType + '_dnase1Log2'] = mean_activity
						REM[cellType + '_samplecount'] = len(matching_samples)
						REM[cellType + '_score'] = mean_score
					else:
						return None

				else:
					if score_thresh[1] <= mean_score <= score_thresh[2] and mean_activity >= activ_thresh:
						# only if the mean score and activity exceeds the  threshold in ALL of the cell types, the REM is
						# returned. If it doesn't exceed the thresh in one cell type, we return None and thus remove it from
						# the output
						REM[cellType + '_dnase1Log2'] = mean_activity
						REM[cellType + '_samplecount'] = len(matching_samples)
						REM[cellType + '_score'] = mean_score
					else:
						return None

			else:  # if there are not thresholds, we can just add the values to the REM
				REM[cellType + '_dnase1Log2'] = mean_activity
				REM[cellType + '_samplecount'] = len(matching_samples)
				REM[cellType + '_score'] = mean_score
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
		return REM
	# get the additional columns for the CREMS
	CREMInfo = CREMAnnotation.objects.filter(REMID=REMID).values()
	if len(CREMInfo) > 0:  # if we the REM belongs to a CREM
		try:
			REM['REMsPerCREM'] = CREMInfo[0]['REMsPerCREM']  # append the attributes
			REM['CREMID'] = CREMInfo[0]['CREMID']
		except IndexError:
			return REM
	else:  # if not, we add the no crem label manually
		REM['REMsPerCREM'] = '-'
		REM['CREMID'] = 'No CREM'

	return REM


# This is only for the detail view when clicking on a CREM-link
def API_CREM_overview(CREMID_list):

	try:
		CREMID_list = list(set(CREMID_list))   # with use of set, we update our query
		# list, so we only have unique values in it
	except TypeError:  # continue if set throws an error
		pass

	hit_list = []
	for crem in CREMID_list:
		try:
			dataset = list(CREMAnnotation.objects.filter(CREMID=crem).values(
				'REMID_id', 'CREMID', 'chr', 'start', 'end', 'REMsPerCREM', 'version', 'REMID_id__geneID', 'REMID_id__geneID__geneSymbol',
				'REMID_id__start',
				'REMID_id__end', 'REMID_id__regressionCoefficient', 'REMID_id__pValue', 'REMID_id__normModelScore'))
		except KeyError:
			continue

	# We don't use the other function, as the dictionary entry has a different name for the CREMs
	# 	for n in range(len(dataset)):
	# 		try:
	# 			dataset[n]['modelScore'] = -math.log2(dataset[n]['REMID_id__pValue'])
	# 		except KeyError:
	# 			dataset[n] = None
		hit_list = hit_list + dataset

	hit_list = [x for x in hit_list if x is not None]  # if a REM's activity in a cell type is under the threshold,

	return hit_list


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
		curr_reg = rem_id['regressionCoefficient']  # get the current regressionCoefficient to calculate the cell type scores
	except KeyError:
		return None
	activity = {}
	stand_activity = {}
	score = {}
	for elem in matching_samples:

		cellType_name = API_celltypeID_celltype(elem['sampleID_id'])  # determines the cellType name from the sampleID
		cellType_name = cellType_name.replace('\"', '')
		if cellType_name in activity.keys():  # take care of tisue or celltypes that occur more than once
			activity[cellType_name] += [elem['dnase1Log2']]
			stand_activity[cellType_name] += [elem['standDnase1Log2']]
		# 	activity[cellType_name] = (float(activity[cellType_name]) + float(elem['dnase1Log2']))/2
		else:
			activity[cellType_name] = [elem['dnase1Log2']]
			stand_activity[cellType_name] = [elem['standDnase1Log2']]
		#
	for cell in activity.keys():
		activity[cell] = np.mean(activity[cell])  # we created a list of all activities we have for this one REMID, now
		# we get the mean of these activity list and take them as new dict entry
		score[cell] = np.mean(stand_activity[cell])

	rem_id['cellTypeScore'] = score  # we add the score in the same format as the activity
	rem_id['cellTypeDNase1Signal'] = activity
	rem_id['geneSymbol'] = geneAnnotation.objects.filter(geneID=rem_id['geneID_id']).values('geneSymbol')[0]['geneSymbol'] # QuerySet
	return rem_id


# The REMID query for the REST_API, also outputs the activity of all celltypes per REM. Every REM is handled separately.
# output fields: chr, start, end, geneID_id, REMID, regressionCoefficient, pValue, version, REMsPerCREM, CREMID, cellTypeActivity -> dictionary of all cell types
def API_REMID_celltype_activity(REMID_list):

	helper = API_REMID(REMID_list)[0]  # determine REMs for the given GeneIDs

	if type(helper) is not list:
		return helper
	hit_list = []
	for i in helper:
		hit_list.append(API_cellType_activity_per_REM(i))
	return hit_list


###############################################################
# NINA HIER! EIN OUTPUT MEHR
###############################################################
# The REMID query. Every REM is handled separately.
def API_REMID(REMID_list, cellTypes_list=[], score_thresh=['no', -1,1], activ_thresh=0.0):

	try:
		REMID_list = list(set(REMID_list))  # with use of set, we update our query
		# list, so we only have unique values in it
	except TypeError:  # continue if set throws an error
		pass

	hit_list = []
	invalid_list = []  # collecting the REM IDs that do not exist in our database

	for i in REMID_list:

		dataset = REMAnnotation.objects.filter(REMID=i).values()  # .values hands back a queryset containing dictionaries

		try:
			this_rem = dataset[0]  # we get back a queryset, with [0] we get it into a dictionary
		except IndexError:
			invalid_list.append(i)
			continue

		# get the additional columns for the CREMS
		this_rem = API_CREM(this_rem)
		this_rem['geneSymbol'] = geneAnnotation.objects.get(geneID=this_rem['geneID_id']).geneSymbol

		# if there are cellTypes that should be filtered for, we do it here for every single REM, to directly add it
		# to the REMs dictionary
		if len(cellTypes_list) > 0:
				this_rem = API_CellTypesActivity(this_rem, cellTypes_list, score_thresh, activ_thresh)

		hit_list.append(this_rem)

	hit_list = [x for x in hit_list if x is not None]  # if a REM's activity in a cell type is under the threshold,
	# we returned None into the list, now we get rid of it

	# hit_list = API_modelScore(hit_list)

	return hit_list, invalid_list  # our list of objects, fitting the query_list


# If a user provides the geneSymbols, we convert them into ENSG format and use the other functions
def API_SymbolToENSG(symbol_list):

	# no need to update the list to unique values, it is done in the main query
	hit_list = []
	invalid_list = []  # collecting the list of symbols that do not exist in the hg38 annotation version
	doublets_list = []
	ensembl_IDs = []
	for symbol in symbol_list:
		try:

			ensembl_IDs = geneAnnotation.objects.filter(geneSymbol=symbol).values()
			for ID in ensembl_IDs:
				hit_list.append(ID['geneID'])
			# if there is more than one ID for the geneSymbol in geneAnnotation (true for 231), we report it in a
			# message box later
			if len(ensembl_IDs) > 1:
				matching_IDs = []
				for i in ensembl_IDs:
					matching_IDs.append(i['geneID'])
				doublets_list.append([symbol, matching_IDs])

		except ObjectDoesNotExist:  # it is very unlikely that an error occurs above, as ensembl ID will just be an empty Queryset
			invalid_list.append(symbol)  # collect all the invalid gene Symbols

		if len(ensembl_IDs) == 0:
			invalid_list.append(symbol)

	return hit_list, list(set(invalid_list)), doublets_list  # our list of objects, fitting the query_list


# The GeneID query for the REST_API, also outputs the activity of all celltypes per REM. Every REM is handled separately.
# output fields: chr, start, end, geneID_id, REMID, regressionCoefficient, pValue, version, REMsPerCREM, CREMID, cellTypeActivity -> dictionary of all cell types
def API_GeneID_celltype_activity(REMID_list):

	helper = API_ENSGID(REMID_list)[0] #determine REMs for the given GeneIDs
	if type(helper) is not list:
		return helper
	hit_list = []
	for i in helper:
		hit_list.append(API_cellType_activity_per_REM(i))  # determine activity
	return hit_list

###############################################################
# NINA HIER! ZWEI OUTPUTS MEHR
###############################################################
# For the GeneID query: given a set of genes, we look up all the REMs for each of them and add
# the additional information
def API_ENSGID(gene_list, cellTypes_list=[], score_thresh=['no', -1,1], activ_thresh=0.0, gene_format='symbol_format'):

	try:
		gene_list = list(set(gene_list))   # with use of set, we update our query
		# list, so we only have unique values in it
	except TypeError:  # continue if set throws an error
		pass

	hit_list = []
	no_hit = []  # report the list of genes that there are no REMs predicted for
	invalid_list = []  # all the wrong formatted inputs that are not existing in the hg38 genome
	for i in gene_list:
		dataset = list(REMAnnotation.objects.filter(geneID=i).values())  # we convert the queryset into a list so we can
		if not dataset:  # if it's empty we have no fitting geneID
			if not list(geneAnnotation.objects.filter(geneID=i).values()):  # if this id is not existent at all
				invalid_list.append(i)
			else:
				no_hit.append(i)

		# add values to it
		for n in range(len(dataset)):

			dataset[n] = API_CREM(dataset[n])
			dataset[n]['geneSymbol'] = geneAnnotation.objects.get(geneID=dataset[n]['geneID_id']).geneSymbol

			if len(cellTypes_list) > 0:
				dataset[n] = API_CellTypesActivity(dataset[n], cellTypes_list, score_thresh, activ_thresh)

		hit_list = hit_list + dataset

	hit_list = [x for x in hit_list if x is not None]  # if a REM's activity in a cell type is under the threshold,
	# we returned None into the list, now we get rid of it

	# hit_list = API_modelScore(hit_list)

	if gene_format == 'symbol_format':  # if there are no REMs for a gene and the user filtered for symbols,
		# we also show the symbols
		for i in range(len(no_hit)):
			no_hit[i] = geneAnnotation.objects.get(geneID=no_hit[i]).geneSymbol

	# print(no_hit)
	# print(invalid_list)
	return hit_list, no_hit, invalid_list


# Is supposed to be used to display the information we have about a gene
def API_ENSGID_geneInfo(gene_list):

	try:
		gene_list = list(set(gene_list))   # with use of set, we update our query
		# list, so we only have unique values in it
	except TypeError:  # continue if set throws an error
		pass

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
def API_Region_celltype_activity(region_list, overlap=100):

	try:
		overlap = float(overlap)
	except TypeError or ValueError:
		overlap = 100

	helper = API_RegionBED(region_list, [], overlap)[0]
	hit_list = []
	for i in helper:
		hit_list.append(API_cellType_activity_per_REM(i))
	return hit_list



# For the GeneRegion query: find all the REMs located in the given regions
# def API_Region(region_list, cellTypes_list=[], overlap=100, activ_tresh=0.0):
#
# 	try:
# 		region_list = [list(x) for x in set(tuple(row) for row in region_list)]  # with use of set, we update our query
# 		# list, so we only have unique values in it
# 	except TypeError:  # if the format wasn't right we continue.
# 		pass
#
# 	hit_list = []
# 	no_hit = []  # collecting the regions that are valid as input but do not contain any REMs
# 	invalid_list = []  # collect the wrongly formatted inputs
#
# 	for i in region_list:
#
# 		try:
# 			# duet to the overlap option, we have 4 scenarios. 1. the rems that overlap completely, 2. the ones that
# 			# overlap but have a lower start position, 3. with a higher end position and 4. those who stick out to
# 			# both ends but still overlap enough
# 			dataset = list(REMAnnotation.objects.filter(chr=i[0]).filter(start__gte=i[1]).filter(end__lte=i[2]).values())
#
# 			if overlap != 100:
# 				dataset_left = list(REMAnnotation.objects.filter(chr=i[0]).filter(end__lt=i[2]).filter(start__lt=i[1]).values())  # REMs that 'stick out' on the left side
# 				dataset_right = list(REMAnnotation.objects.filter(chr=i[0]).filter(start__gt=i[1]).filter(end__gt=i[2]).values())
# 				dataset_both = list(REMAnnotation.objects.filter(chr=i[0]).filter(start__lt=i[1]).filter(end__gt=i[2]).values())
#
# 				for n in dataset_left:
# 					if int(i[1]) - int(n['start']) <= (int(n['end'])-int(n['start']))*(overlap/100):
# 						dataset.append(n)
# 				for n in dataset_right:
# 					if int(n['end']) - int(i[2]) <= (int(n['end'])-int(n['start']))*(overlap/100):
# 						dataset.append(n)
# 				for n in dataset_both:
# 					if int(n['end']) - int(i[2]) + int(i[1]) - int(n['start']) <= (int(n['end'])-int(n['start']))*(overlap/100):
# 						dataset.append(n)
# 			# check for valid input without a dataset, everything else is considered invalid, meaning start greater
# 			# than end or not a valid chr, only necessary if there is no data found, otherwise there would be a result
# 			if len(dataset) == 0:  # if it is empty it could also be that the input is valid but there is no REM
# 				if i[0][3:] in ['X', 'Y']:  # first check the 'string' chromosomes
# 					try:
# 						if int(i[1]) < int(i[2]):
# 							no_hit.append(i)
# 						else:
# 							invalid_list.append(i)
# 					except ValueError:  # meaning that start and ends are no ints
# 						invalid_list.append(i)
# 				else:
# 					try:
# 						if 0 < int(i[0][3:]) < 23 and int(i[1]) < int(i[2]):  # check whether the chromosome number is
# 							# in range and whether start and end are valid ints
# 							no_hit.append(i)
# 						else:
# 							invalid_list.append(i)
#
# 					except ValueError:
# 						invalid_list.append(i)
#
# 			for n in range(len(dataset)):
# 				dataset[n] = API_CREM(dataset[n])
# 				dataset[n]['geneSymbol'] = geneAnnotation.objects.get(geneID=dataset[n]['geneID_id']).geneSymbol
#
# 				if len(cellTypes_list) > 0:
# 					dataset[n] = API_CellTypesActivity(dataset[n], cellTypes_list, activ_tresh)
#
# 		except (ValueError, IndexError, KeyError):  # everything throwing an error now, should be caused by an invalid
# 			# input
# 			invalid_list.append(i)
# 			continue
#
# 		hit_list = hit_list + dataset
#
# 	hit_list = [x for x in hit_list if x is not None]  # if a REM's activity in a cell type is under the threshold,
# 	# we returned None into the list, now we get rid of it
#
# 	# hit_list = API_modelScore(hit_list)
#
# 	return hit_list, no_hit, invalid_list  # our list of dictionaries, fitting the query_list


def API_RegionBED(region_list, cellTypes_list=[], overlap='F', score_thresh=['no', -1,1], activ_thresh=0.0):

	try:
		region_list = [list(x) for x in set(tuple(row) for row in region_list)]  # with use of set, we update our query
		# list, so we only have unique values in it
	except TypeError:  # if the format wasn't right we continue.
		pass

	hit_list = []
	# no_hit = []  # collecting the regions that are valid as input but do not contain any REMs
	invalid_list = []  # collect the wrongly formatted inputs
	REM_bed_file = 'static/REMAnnotation.bed'
	corr_region_list = []

	for i in region_list:
		if i[0][3:] in ['X', 'Y', 'x', 'y']:  # first check the 'string' chromosomes
			try:
				if int(i[1]) < int(i[2]):
					corr_region_list.append(i)
					# no_hit.append(i)
				else:
					invalid_list.append(i)
			except ValueError:  # meaning that start and ends are no ints
				invalid_list.append(i)
		else:
			try:
				if 0 < int(i[0][3:]) < 23 and int(i[1]) < int(i[2]):  # check whether the chromosome number is
					# in range and whether start and end are valid ints
					# no_hit.append(i)
					corr_region_list.append(i)
				else:
					invalid_list.append(i)

			except ValueError:
				invalid_list.append(i)

	region = ''
	for i in corr_region_list:
		region += '\t'.join(i) + '\n'

	region_bed = BedTool(region, from_string=True)
	if overlap == 'F':  # if there was no overlap chosen, we report only REMs that lie completely within the regions
		hits = region_bed.intersect(REM_bed_file, F=1, wb=True)
	else:
		hits = region_bed.intersect(REM_bed_file, f=overlap/100, wb=True)
	rem_hit_list = [x[6] for x in hits]

	try:
		# due to the overlap option, we have 4 scenarios. 1. the rems that overlap completely, 2. the ones that
		# overlap but have a lower start position, 3. with a higher end position and 4. those who stick out to
		# both ends but still overlap enough
		dataset = list(REMAnnotation.objects.filter(REMID__in=rem_hit_list).values())

		# check for valid input without a dataset, everything else is considered invalid, meaning start greater
		# than end or not a valid chr, only necessary if there is no data found, otherwise there would be a result
		for n in range(len(dataset)):
			dataset[n] = API_CREM(dataset[n])
			dataset[n]['geneSymbol'] = geneAnnotation.objects.get(geneID=dataset[n]['geneID_id']).geneSymbol

			if len(cellTypes_list) > 0:
				dataset[n] = API_CellTypesActivity(dataset[n], cellTypes_list, score_thresh, activ_thresh)
		hit_list = hit_list + dataset

	except (ValueError, IndexError, KeyError):  # everything throwing an error now, should be caused by an invalid
		# input
		pass

	hit_list = [x for x in hit_list if x is not None]  # if a REM's activity in a cell type is under the threshold,
	# we returned None into the list, now we get rid of it

	# hit_list = API_modelScore(hit_list)
	return hit_list, invalid_list  # our list of dictionaries, fitting the query_list
