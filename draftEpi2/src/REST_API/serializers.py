from rest_framework import serializers
from table_manager.models import geneAnnotation, REMAnnotation


class GeneInfoAllSerializer(serializers.ModelSerializer):

	""" information displayed with url /REST_API/GeneInfo/ """
	class Meta:
		model = geneAnnotation
		fields = ['geneID']


class GeneInfoSerializer(serializers.ModelSerializer):

	""" information displayed with url /REST_API/GeneInfo/<GeneID>/ """
	class Meta:
		model = geneAnnotation
		fields = ('geneID', 'chr', 'start', 'end', 'geneSymbol', 'alternativeGeneID', 'strand', 'annotationVersion_id')
		#fields = '__all__'


class REMInfoAllSerializer(serializers.ModelSerializer):

	""" information displayed with url /REST_API/REMInfo/<REMID>/ """
	class Meta:
		model = REMAnnotation
		#fields = '__all__'
		fields = ('REMID')


class REMInfoSerializer(serializers.Serializer):
	
	""" information displayed with url /REST_API/REMInfo/<REMID>/ """

	REMID = serializers.CharField(max_length=30)
	chr = serializers.CharField(max_length=10)
	start = serializers.IntegerField()
	end = serializers.IntegerField()
	geneID = serializers.CharField(source='geneID_id') #rename field name (source is the name of the filed in the dict
	regressionCoefficient = serializers.FloatField()
	pValue = serializers.FloatField()
#	version = serializers.IntegerField()
	REMsPerCREM = serializers.IntegerField()
	CREMID = serializers.CharField()
	cellTypeActivity = serializers.DictField(child=serializers.FloatField())

