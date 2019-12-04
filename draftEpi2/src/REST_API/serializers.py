from rest_framework import serializers
from table_manager.models import geneAnnotation
#from .models import geneAnnotation 


class GeneAnnotationSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = geneAnnotation
		#fields = ('chr', 'start', 'end', 'geneID', 'geneSymbol', 'alternativeGeneID', 'isTF', 'strand', 'annotationVersion')
		fileds = '__all__'
	 
