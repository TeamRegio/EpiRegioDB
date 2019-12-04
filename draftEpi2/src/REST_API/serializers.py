from rest_framework import serializers
from table_manager.models import geneAnnotation, REMAnnotation


class GeneInfoSerializer(serializers.ModelSerializer):

	class Meta:
		model = geneAnnotation
		fields = ('chr', 'start', 'end', 'geneID', 'geneSymbol', 'alternativeGeneID', 'strand', 'annotationVersion_id')
		#fields = '__all__'

class REMInfoSerializer(serializers.ModelSerializer):

	class Meta:
		model = REMAnnotation #it is only possible to return the fileds of the table REMAnnotation, the API also return the CREMID whichis not possible to display here. Thats because I based the serializer on the models. It is also possible to do it in a models indepent way. Do we prefer this?
		#fields = '__all__'
		fields = ('chr', 'start', 'end', 'geneID_id', 'REMID', 'regressionCoefficient', 'pValue')



