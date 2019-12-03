from rest_framework import serializers
from models import geneAnnotation 


class GeneAnnotationSerializer(Serializers.ModelSerializer):
	
	class Meta:
		model = GeneAnnotation
		#fields = ('chr', 'start', 'end', 'geneID', 'geneSymbol', 'alternativeGeneID', 'isTF', 'strand', 'annotationVersion')
		fileds = '__all__'
	 
