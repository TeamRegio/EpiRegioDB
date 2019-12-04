#from django.db import models

# Create your models here.
#
from table_manager.models import geneAnnotation

#class geneInfo(models.Model):
#	chr = models.CharField(max_length = 10)
#	start =  models.IntegerField()
#	end =  models.IntegerField()
#	geneID = models.CharField(max_length = 40)
#	geneSymbol = models.CharField(max_length=30)
#	alternativeGeneID = models.CharField(max_length=30)
#	isTF = models.BooleanField() 
#	strand = models.CharField(max_length=10)
#	annotationVersion = models.CharField(max_length= 100)
#
#	def __str__(self):
#		return self.geneID
