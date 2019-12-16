from rest_framework import serializers
from table_manager.models import geneAnnotation, REMAnnotation


#class GeneInfoAllSerializer(serializers.ModelSerializer):
#
#	""" information displayed with url /REST_API/GeneInfo/ """
#	class Meta:
#		model = geneAnnotation
#		fields = ['geneID']


class GeneInfoSerializer(serializers.ModelSerializer):
	annotationVersion = serializers.CharField(source='annotationVersion_id')

	""" information displayed with url /REST_API/GeneInfo/<GeneID>/ """
	class Meta:
		model = geneAnnotation
		fields = ('geneID', 'chr', 'start', 'end', 'geneSymbol', 'alternativeGeneID', 'strand', 'annotationVersion')
		#fields = '__all__'


#class REMInfoAllSerializer(serializers.ModelSerializer):
#
#	""" information displayed with url /REST_API/REMInfo/<REMID>/ """
#	class Meta:
#		model = REMAnnotation
#		#fields = '__all__'
#		fields = ('REMID')


class REMQuerySerializer(serializers.Serializer):
	
	""" information displayed with url /REST_API/REMInfo/<REMID>/ """

	REMID = serializers.CharField(max_length=30)
	chr = serializers.CharField(max_length=10)
	start = serializers.IntegerField()
	end = serializers.IntegerField()
	geneID = serializers.CharField(source='geneID_id') #rename field name (source is the name of the filed in the dict
	geneSymbol = serializers.CharField()
	regressionCoefficient = serializers.FloatField()
	pValue = serializers.FloatField()
	version = serializers.IntegerField()
	REMsPerCREM = serializers.IntegerField()
	CREMID = serializers.CharField()
	cellTypeActivity = serializers.DictField(child=serializers.FloatField())


class CREMQuerySerializer(serializers.Serializer):

	""" information displayed with url /REST_API/CREMInfo/<CREM_id> """
	
	CREMID = serializers.CharField()
	chr = serializers.CharField()
	start = serializers.IntegerField()
	end = serializers.IntegerField()
	REMsPerCREM = serializers.IntegerField()
	REMID = serializers.CharField(source = 'REMID_id')
	linkedGene = serializers.CharField(source='REMID_id__geneID')
	REM_Start = serializers.IntegerField(source = 'REMID_id__start')
	REM_End = serializers.IntegerField(source = 'REMID_id__end')
	REM_RegressionCoefficient = serializers.FloatField(source = 'REMID_id__regressionCoefficient')
	REM_Pvalue = serializers.FloatField(source = 'REMID_id__pValue')
	version = serializers.IntegerField()
	

class GeneQuerySerializer(serializers.Serializer):
	geneID = serializers.CharField(source='geneID_id') #rename field name (source is the name of the filed in the dict
	geneSymbol = serializers.CharField()
	REMID = serializers.CharField(max_length=30)
	chr = serializers.CharField(max_length=10)
	start = serializers.IntegerField()
	end = serializers.IntegerField()
	regressionCoefficient = serializers.FloatField()
	pValue = serializers.FloatField()
	version = serializers.IntegerField()
	REMsPerCREM = serializers.IntegerField()
	CREMID = serializers.CharField()
	cellTypeActivity = serializers.DictField(child=serializers.FloatField())

class RegionQuerySerializer(serializers.Serializer):
	geneID = serializers.CharField(source='geneID_id') #rename field name (source is the name of the filed in the dict
	geneSymbol = serializers.CharField()
	REMID = serializers.CharField(max_length=30)
	chr = serializers.CharField(max_length=10)
	start = serializers.IntegerField()
	end = serializers.IntegerField()
	regressionCoefficient = serializers.FloatField()
	pValue = serializers.FloatField()
	version = serializers.IntegerField()
	REMsPerCREM = serializers.IntegerField()
	CREMID = serializers.CharField()
	cellTypeActivity = serializers.DictField(child=serializers.FloatField())





