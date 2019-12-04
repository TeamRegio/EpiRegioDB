from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#from rest_framework.decorators import api_view
#from .models import geneInfo

from .serializers import GeneInfoSerializer, REMInfoSerializer

#for testing
from table_manager.models import geneAnnotation, REMAnnotation 

#import sys
#sys.path.insert(1, r'../')#tell python the path of the project
from API import  API_ENSGID_geneInfo, API_REMID 
#url /geneID/
class GeneInfo(APIView):

	#TODO: catch errors, I gues this should happen in the API file	
	def get(self,request, gene_id):
	#	try:
		#test example [0] is necessary to get first element from querySet (set of dictionary or something similar)
		#gene = geneAnnotation.objects.filter(geneID = gene_id).values()[0]

		#using API function. Since this is a list of query-sets, we need[0] to get the query-set and the second one to geth the first dictionary
		gene = API_ENSGID_geneInfo([gene_id])[0][0]
		print(gene)

		serializers = GeneInfoSerializer(gene) # , many = True) wenn man mehrer objects zuruekgeben mag
		return Response(serializers.data)
		#except GeneId.DoesNotExist:
		#	return Response(status=status.HTTP_404_NOT_FOUND)
		
#TODO: This takes some time ... Do we want to have this functionality?
class GenesInfo(APIView):
	def get(self,request):
		genes = geneAnnotation.objects.all()

		serializers = GeneInfoSerializer(genes, many = True) #wenn man mehrer objects zuruekgeben mag
		return Response(serializers.data)

class REMInfo(APIView):

	def get(self, request,REM_id):
		REM = API_REMID([REM_id], [])[0] #empty cellTypeList
		serializers = REMInfoSerializer(REM) # , many = True) wenn man mehrer objects zuruekgeben mag
		return Response(serializers.data)


#TODO: This takes some time ... Do we want to have this functionality?
class REMsInfo(APIView):

	def get(self, request):
		REMs = REMAnnotation.objects.all()
		serializers = REMInfoSerializer(REMs , many = True)# wenn man mehrer objects zuruekgeben mag
		return Response(serializers.data)
