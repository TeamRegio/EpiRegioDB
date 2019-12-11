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


def parseRequest(request, sep, start, end, keyword):
	#parse input
	request_list = request.split(sep)
	output_list = []
	for i in request_list:
		if i[start:end] == keyword: #check if the element of the request is a REMID
			output_list.append(i)
		else:
			#return error message
			return 0
	return output_list



#url /geneID/
#model.serializers
class GeneInfo(APIView):
	"""display all Info we store for a gene """
	#TODO: catch errors, I gues this should happen in the API file	
	def get(self,request, gene_id):
		gene_id_list = parseRequest(gene_id, '_', 0, 4, 'ENSG')
		if gene_id_list == 0: #check if input is valid
			return Response(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
	#	try:
		#test example [0] is necessary to get first element from querySet (set of dictionary or something similar)
		#gene = geneAnnotation.objects.filter(geneID = gene_id).values()[0]

		#using API function. Since this is a list of query-sets, we need[0] to get the query-set and the second one to geth the first dictionary
		#gene = API_ENSGID_geneInfo([gene_id])[0][0]
		gene = API_ENSGID_geneInfo(gene_id_list)

		serializers = GeneInfoSerializer(gene, many = True) #wenn man mehrer objects zuruekgeben mag
		return Response(serializers.data)
		#except GeneId.DoesNotExist:
		#	return Response(status=status.HTTP_404_NOT_FOUND)
		
#serialisers
@api_view(['GET'])
def REMInfo(request, REM_id):
	""" displays info about REMs, how many REMs we stored per CREM and the corresponding CREMId"""
	if request.method == 'GET':
		#parse input
		REM_id_list = parseRequest(REM_id, '_', 0, 3, 'REM')
		if REM_id_list == 0: #check if input is valid
			return Response(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

		#call API function to get REM info
		REM = API_REMID_celltype_activity(REM_id_list)
		print(REM)
		serializers = REMInfoSerializer(REM, many = True) #wenn man mehrer objects zuruekgeben mag
		return Response(serializers.data)


#serialisers
@api_view(['GET'])
def CREMInfo(request, CREM_id):
	""" displays info about REMs, how many REMs we stored per CREM and the corresponding CREMId"""
	if request.method == 'GET':
		#parse input
		CREM_id_list = parseRequest(CREM_id, '_', 0, 4, 'CREM')
		if CREM_id_list == 0: #check if input is valid
			return Response(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
		print(CREM_id_list)
		#call API function to get REM info
		CREM = API_CREM_overview(CREM_id_list)
		print(CREM)
		serializers = CREMInfoSerializer(CREM, many = True) #wenn man mehrer objects zuruekgeben mag
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

