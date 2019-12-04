from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import geneAnnotation
from .serializers import GeneAnnotationSerializer

#url /geneID/
class GeneAnnotation(APIView):
	
	def get(self, request):
		gene = GeneAnnotation.objects.get(geneID = 'ENSG00000223972')
		serializers = GeneAnnotationSerializer(gene) # , many = True) wenn man mehrer objects zuruekgeben mag
		return Response(serializers.data)

