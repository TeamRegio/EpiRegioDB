from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import status
#from .models import geneInfo

#from .serializers import GeneInfoSerializer, REMInfoSerializer
from .serializers import *

#for testing
from table_manager.models import geneAnnotation, REMAnnotation 

from API import  *


def parseRequest(request, sep, start, end, keyword, region = 0):
	#parse input
	request_list = request.split(sep)
	output_list = []
	if keyword == '':
		return request_list
	for i in request_list:
		if i[start:end] == keyword: #check if the element of the request is a REMID
			output_list.append(i)
			#RegionQuery - checks if reuest has the write format
			if region == 1:
				if i.count(":") != 1 or i.count("-") != 1:
					return i
				else:
					helper = i.split(':')
					helper_2 = helper[1].split("-")
					if float(helper_2[0]) > float(helper_2[1]):
						return i
		else:
			#return error message
			return i
	return output_list


#url /geneID/
#model.serializers
class GeneInfo(APIView):
	""" displays per input Ensmbl ID (e.g. ENSG00000223972) general gene information """
	def get(self,request, gene_id):
		gene_id_list = parseRequest(gene_id, '_', 0, 4, 'ENSG')
		if type(gene_id_list) is not list:  #check if input is valid
			serializers = ErrorSerializer({'info' : "Error - given Gene ID is not valid " + gene_id_list})
			return Response(serializers.data)
		gene = API_ENSGID_geneInfo(gene_id_list)
		if gene == []: 
			serializers = ErrorSerializer({'info' : "Error - at least one given Gene ID is not valid"})
			return Response(serializers.data)
			#return Response(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

		serializers = GeneInfoSerializer(gene, many = True) #wenn man mehrer objects zuruekgeben mag
		return Response(serializers.data)
		
#serialisers
@api_view(['GET'])
def REMQuery(request, REM_id):
	""" displays information about the input regulatory element(s) (e.g. REM0192593) """
	if request.method == 'GET':
		#parse input
		#REM_id_list = parseRequest(REM_id, '_', 0, 3, 'REM')
		REM_id_list = parseRequest(REM_id, '_', 0, 3, '') #done in API function
	#	if REM_id_list == 0: #check if input is valid
	#		return Response(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

		#call API function to get REM info
		REM = API_REMID_celltype_activity(REM_id_list)
		if type(REM) is list:
			serializers = REMQuerySerializer(REM, many = True) #wenn man mehrer objects zuruekgeben mag
		else:
			serializers = ErrorSerializer({'info' : REM})

		return Response(serializers.data)


#serialisers
@api_view(['GET'])
def CREMQuery(request, CREM_id):
	""" lists per input CREM ID (e.g. CREM0192593) all associated REMs seperatly """
	if request.method == 'GET':
		#parse input
		CREM_id_list = parseRequest(CREM_id, '_', 0, 4, 'CREM')
		if type(CREM_id_list) is not list:  #check if input is valid
			serializers = ErrorSerializer({'info' : "Error - given CREM ID is not valid " + CREM_id_list})
			return Response(serializers.data)
		#	return Response(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
		#call API function to get REM info
		CREM = API_CREM_overview(CREM_id_list)
		if CREM == []:
			serializers = ErrorSerializer({'info' : "Error - at least one given CREM ID is not valid"})
			return Response(serializers.data)
			#return Response(status=status.HTTP_404_NOT_FOUND)
		serializers = CREMQuerySerializer(CREM, many = True) #wenn man mehrer objects zuruekgeben mag
		return Response(serializers.data)

#serialisers
@api_view(['GET'])
def GeneQuery(request, gene_id):
	""" displays for each Gene ID (e.g. ENSG00000223972) the associated REMs seperatly"""
	if request.method == 'GET':
		#parse input
		#gene_id_list = parseRequest(gene_id, '_', 0, 4, 'ENSG')
		gene_id_list = parseRequest(gene_id, '_', 0, 0, '') #done by API function
#		if gene_id_list == 0: #check if input is valid
		#	return Response(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

		#call API function to get REM info
		REM = API_GeneID_celltype_activity(gene_id_list)
		if type(REM) is list:
			serializers = GeneQuerySerializer(REM, many = True) #wenn man mehrer objects zuruekgeben mag
		else:
			serializers = ErrorSerializer({'info' : REM})
		return Response(serializers.data)

@api_view(['GET'])
def RegionQuery(request, region, overlap='100/'):
	""" displays for each input region chr:start-end with start <= end (e.g. chr16:75423948-75424405) all REMs which are contained in it """
	if request.method == 'GET':
		#parse input
		# Dennis api function test if start is smaller or equal than end
		# TODO: check if is is the correct format with : and -
		helper_list = parseRequest(region, '_', 0, 3, 'chr', 1)
		if type(helper_list) is not list:  #check if input is valid
			serializers = ErrorSerializer({'info' : "Error - given region is not valid " + helper_list})
			return Response(serializers.data)

		try:
			overlap = overlap[:-1]  # overlap till -1 as we have a slash at the end to have it optional in the url
		except TypeError:
			overlap = 100
#			return Response(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
		#parse chr:start-end in list format
		region_list = []
		for i in helper_list:
			h1 = i.split(":")
			h2 = h1[1].split("-")
			region_list.append([h1[0], h2[0], h2[1]])
		#call API function to get REM info
		REM = API_Region_celltype_activity(region_list, overlap)
		serializers = RegionQuerySerializer(REM, many = True) #wenn man mehrer objects zuruekgeben mag
		return Response(serializers.data)

#TODO: This takes some time ... Do we want to have this functionality?
#class GeneInfoAll(APIView):
#	def get(self,request):
#		genes = geneAnnotation.objects.all()
#
#		serializers = GeneInfoAllSerializer(genes, many = True) #wenn man mehrer objects zuruekgeben mag
#		return Response(serializers.data)

#class REMInfo(APIView):
#
#	def get(self, request,REM_id):
#		REM = API_REMID([REM_id], [], 0.0)[0] #empty cellTypeList
#		print(REM)
#		serializers = REMInfoSerializer(REM) # , many = True) wenn man mehrer objects zuruekgeben mag
#		return Response(serializers.data)


#TODO: This takes some time ... Do we want to have this functionality?
#class REMInfoAll(APIView):
#
#	def get(self, request):
#		REMs = REMAnnotation.objects.all()
#		serializers = REMInfoAllSerializer(REMs , many = True)# wenn man mehrer objects zuruekgeben mag
#		return Response(serializers.data)

