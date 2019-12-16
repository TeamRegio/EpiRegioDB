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
	for i in request_list:
		if i[start:end] == keyword: #check if the element of the request is a REMID
			output_list.append(i)
			#RegionQuery - checks if reuest has the write format
			if region == 1:
				if i.count(":") != 1 or i.count("-") != 1:
					return 0
		else:
			#return error message
			return 0
	return output_list


#url /geneID/
#model.serializers
class GeneInfo(APIView):
	""" displays per input Gene ID (e.g. ENSG00000223972) general gene information """
	def get(self,request, gene_id):
		gene_id_list = parseRequest(gene_id, '_', 0, 4, 'ENSG')
		if gene_id_list == 0: #check if input is valid
			return Response(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
		gene = API_ENSGID_geneInfo(gene_id_list)
		if gene == None: 
			return Response(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

		serializers = GeneInfoSerializer(gene, many = True) #wenn man mehrer objects zuruekgeben mag
		return Response(serializers.data)
		
#serialisers
@api_view(['GET'])
def REMQuery(request, REM_id):
	""" displays information about the input regulatory elements (e.g. REM0192593) """
	if request.method == 'GET':
		#parse input
		REM_id_list = parseRequest(REM_id, '_', 0, 3, 'REM')
		if REM_id_list == 0: #check if input is valid
			return Response(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

		#call API function to get REM info
		REM = API_REMID_celltype_activity(REM_id_list)
		serializers = REMQuerySerializer(REM, many = True) #wenn man mehrer objects zuruekgeben mag
		return Response(serializers.data)


#serialisers
@api_view(['GET'])
def CREMQuery(request, CREM_id):
	""" lists per input CREM ID (e.g. CREM0192593) all associated REMs seperatly """
	if request.method == 'GET':
		#parse input
		CREM_id_list = parseRequest(CREM_id, '_', 0, 4, 'CREM')
		if CREM_id_list == 0: #check if input is valid
			return Response(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
		print(CREM_id_list)
		#call API function to get REM info
		CREM = API_CREM_overview(CREM_id_list)
		print(CREM)
		if CREM == []:
			return Response(status=status.HTTP_404_NOT_FOUND)
		serializers = CREMQuerySerializer(CREM, many = True) #wenn man mehrer objects zuruekgeben mag
		return Response(serializers.data)

#serialisers
@api_view(['GET'])
def GeneQuery(request, gene_id):
	""" displays for each Gene ID (e.g. ENSG00000223972) the associated REMs seperatly"""
	if request.method == 'GET':
		#parse input
		gene_id_list = parseRequest(gene_id, '_', 0, 4, 'ENSG')
		if gene_id_list == 0: #check if input is valid
			return Response(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

		#call API function to get REM info
		REM = API_GeneID_celltype_activity(gene_id_list)
		serializers = GeneQuerySerializer(REM, many = True) #wenn man mehrer objects zuruekgeben mag
		return Response(serializers.data)


@api_view(['GET'])
def RegionQuery(request, region):
	""" displays for each input region (e.g. chr16:75423948-75424405 with start<=end) all overlappin REMs """
	if request.method == 'GET':
		#parse input
		# Dennis api function test if start is smaller or equal than end
		# TODO: check if is is the correct format with : and -
		helper_list = parseRequest(region, '_', 0, 3, 'chr', 1)
		if helper_list == 0: #check if input is valid
			return Response(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
		#parse chr:start-end in list format
		region_list = []
		for i in helper_list:
			h1 = i.split(":")
			h2 = h1[1].split("-")
			region_list.append([h1[0], h2[0], h2[1]])
		#call API function to get REM info
		REM = API_Region_celltype_activity(region_list)
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

