# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


# ==========================================================================
class genomeAnnotation(models.Model):
    genomeVersion = models.CharField(max_length=4, blank=True)
    annotationVersion = models.CharField(max_length=3, primary_key=True)
    databaseName = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = True  # has to be set to True, as unittesting requires creating a test object
        db_table = 'genomeAnnotation'

    def __str__(self):
        return (str(self.genomeVersion) +  " " + str(self.annotationVersion) + " " + str(self.databaseName))


# ==========================================================================
class cellTypes(models.Model):
    cellTypeID = models.CharField(max_length=255, primary_key=True)
    cellTypeName = models.CharField(max_length=255, blank=True)
    cellOntologyTerm = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = True
        db_table = 'cellTypes'

    def __str__(self):
        return (str(self.cellTypeID) + " " + str(self.cellTypeName) + " " + str(self.cellOntologyTerm))


# ==========================================================================
class geneAnnotation(models.Model):
    chr = models.CharField(max_length=10, blank=True)
    start = models.IntegerField(blank=True)
    end = models.IntegerField(blank=True)
    geneID = models.CharField(max_length=255, primary_key=True)
    geneSymbol = models.CharField(max_length=255, blank=True)
    alternativeGeneID = models.CharField(max_length=255, blank=True)
    isTF = models.CharField(max_length=255, blank=True, null=True)
    strand = models.CharField(max_length=1, blank=True)
    annotationVersion = models.ForeignKey(genomeAnnotation, to_field="annotationVersion",db_column='annotationVersion', on_delete=models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'geneAnnotation'

    def __str__(self):
        return (str(self.geneID) + " " + str(self.chr) + ":" + str(self.start) + "-" + str(self.end) + " "  + str(self.geneSymbol) + " " + str(self.isTF) + " " + str(self.strand) + " " + str(self.annotationVersion))


# ==========================================================================
class REMAnnotation(models.Model):
    chr = models.CharField(max_length=10, blank=True)
    start = models.IntegerField(blank=True)
    end = models.IntegerField(blank=True)
    geneID = models.ForeignKey(geneAnnotation, to_field="geneID", db_column='geneID', on_delete=models.DO_NOTHING)
    REMID = models.CharField(max_length=255, primary_key=True)
    regressionCoefficient = models.FloatField(blank=True)
    pValue = models.FloatField(blank=True)
    version = models.CharField(max_length=1, blank=True)

    class Meta:
        managed = True
        db_table = 'REMAnnotation'

    def __str__(self):
        return (str(self.REMID)  +  " " + str(self.chr) + ":" + str(self.start) + "-" + str(self.end))


# ==========================================================================
class sampleInfo(models.Model):
    sampleID = models.CharField(max_length=255, primary_key=True)
    originalSampleID = models.CharField(max_length=255, blank=True)
    cellTypeID = models.ForeignKey(cellTypes, to_field="cellTypeID", db_column='cellTypeID', on_delete=models.DO_NOTHING)
    origin = models.CharField(max_length=255, blank=True)
    dataType = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = True
        db_table = 'sampleInfo'

    def __str__(self):
        return (str(self.sampleID) + " " + str(self.originalSampleID) + " " + str(self.cellTypeID) + " " + str(self.origin) + " " + str(self.dataType))


# ==========================================================================
class geneExpression(models.Model):
    class Meta:
        managed = True
        db_table = 'geneExpression'
        # unique_together = (('geneID', 'sampleID'),)

    """ We set the geneID here as OneToOneField and as primary key. It works like a Foreign key that is supposed 
    to be unique but the “reverse” side of the relation will directly return a single object. We need a replacement for 
    a primary key, so the object.get works. Filter also works with only foreign keys. We do the same for 
    REMActivity."""

    geneID = models.OneToOneField(geneAnnotation, to_field="geneID", db_column='geneID', primary_key=True, on_delete=models.DO_NOTHING)
    sampleID = models.ForeignKey(sampleInfo, to_field="sampleID", db_column='sampleID', on_delete=models.DO_NOTHING)
    expressionLog2TPM = models.FloatField(blank=True)
    species = models.CharField(max_length=255)

    def __str__(self):
        return str(str(self.geneID) + ' ' + str(self.sampleID) + ' ' + str(self.expressionLog2TPM))


# ==========================================================================
class REMActivity(models.Model):

    class Meta:
        managed = True
        db_table = 'REMActivity'
        # unique_together = (('REMID', 'sampleID'))

    REMID = models.OneToOneField(REMAnnotation, to_field="REMID", db_column='REMID', primary_key=True, on_delete=models.DO_NOTHING)
    sampleID = models.ForeignKey(sampleInfo, to_field="sampleID", db_column='sampleID', on_delete=models.DO_NOTHING)
    dnase1Log2 = models.FloatField(blank=True)
    version = models.CharField(max_length=1, blank=True)

    def __str__(self):
        return str(str(self.REMID))


# ==========================================================================
class CREMAnnotation(models.Model):
    class Meta:
        managed = True
        db_table = 'CREMAnnotation'

    REMID = models.OneToOneField(REMAnnotation, to_field="REMID", db_column="REMID", max_length=30, primary_key=True, on_delete=models.DO_NOTHING)
    CREMID = models.CharField(max_length=255)
    chr = models.CharField(max_length=10, blank=True)
    start = models.IntegerField(blank=True)
    end = models.IntegerField(blank=True)
    REMsPerCREM = models.IntegerField(blank=True)
    version = models.IntegerField(blank=True)
