from django.test import TestCase

# Create your tests here.
from table_manager.models import *
# All the functions have to start with 'test' to be called by the manage.py test command

# ==========================================================================
# MODEL TESTING
# ==========================================================================

class genomeAnnotationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        print('Model Test - genomeAnnotation')
        genomeAnnotation.objects.create(annotationVersion='the', genomeVersion='best',  databaseName='chocolate')

    def test_genomeAnnotation_label(self):
        test_obj = genomeAnnotation.objects.get(annotationVersion='the')
        field_label0 = test_obj._meta.get_field('genomeVersion').verbose_name
        field_label1 = test_obj._meta.get_field('annotationVersion').verbose_name
        field_label2 = test_obj._meta.get_field('databaseName').verbose_name
        field_labels = [field_label0, field_label1, field_label2]
        self.assertEquals(field_labels, ['genomeVersion', 'annotationVersion', 'databaseName'])

    def test_genomeAnnotation_max_length(self):
        test_obj = genomeAnnotation.objects.get(annotationVersion='the')
        max_length0 = test_obj._meta.get_field('genomeVersion').max_length
        max_length1 = test_obj._meta.get_field('annotationVersion').max_length
        max_length2 = test_obj._meta.get_field('databaseName').max_length
        max_lengths = [max_length0, max_length1, max_length2]
        self.assertEquals(max_lengths, [4, 3, 255])

    def test_genomeAnnotation_string(self):  # also shows that all attributes were assigned correctly
        test_obj = genomeAnnotation.objects.get(annotationVersion='the')
        expected_object_name = str(test_obj.genomeVersion) + " " + str(test_obj.annotationVersion) + " " + str(test_obj.databaseName)
        self.assertEquals(expected_object_name, str(test_obj))


class cellTypesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        print('Model Test - cellTypes')
        cellTypes.objects.create(cellTypeID='chip', cellTypeName='cookies', cellOntologyTerm='ingredients:')

    def test_cellType_label(self):
        test_obj = cellTypes.objects.get(cellTypeID='chip')
        field_label0 = test_obj._meta.get_field('cellTypeID').verbose_name
        field_label1 = test_obj._meta.get_field('cellTypeName').verbose_name
        field_label2 = test_obj._meta.get_field('cellOntologyTerm').verbose_name
        field_labels = [field_label0, field_label1, field_label2]
        self.assertEquals(field_labels, ['cellTypeID', 'cellTypeName', 'cellOntologyTerm'])

    def test_cellTypes_max_length(self):
        test_obj = cellTypes.objects.get(cellTypeID='chip')
        max_length0 = test_obj._meta.get_field('cellTypeID').max_length
        max_length1 = test_obj._meta.get_field('cellTypeName').max_length
        max_length2 = test_obj._meta.get_field('cellOntologyTerm').max_length
        max_lengths = [max_length0, max_length1, max_length2]
        self.assertEquals(max_lengths, [255, 255, 255])

    def test_cellTypes_string(self):  # also shows that all attributes were assigned correctly
        test_obj = cellTypes.objects.get(cellTypeID='chip')
        expected_object_name = str(test_obj.cellTypeID) + " " + str(test_obj.cellTypeName) + " " + str(test_obj.cellOntologyTerm)
        self.assertEquals(expected_object_name, str(test_obj))


class geneAnnotationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # We first need the genome Annotation instance as annotationVersion is a FK of it
        print('Model Test - geneAnnotation')
        genomeAnnotation.objects.create(annotationVersion='the', genomeVersion='best',  databaseName='chocolate')
        geneAnnotation.objects.create(chr='250gButter', start=1, end=2, geneID='200gBrownSugar', geneSymbol='175gSugar', alternativeGeneID='2Eggs', isTF='375gFlour', strand='+', annotationVersion_id='the')

    def test_geneAnnotation_label(self):
        test_obj = geneAnnotation.objects.get(geneID='200gBrownSugar')
        field_label0 = test_obj._meta.get_field('chr').verbose_name
        field_label1 = test_obj._meta.get_field('start').verbose_name
        field_label2 = test_obj._meta.get_field('end').verbose_name
        field_label3 = test_obj._meta.get_field('geneID').verbose_name
        field_label4 = test_obj._meta.get_field('geneSymbol').verbose_name
        field_label5 = test_obj._meta.get_field('alternativeGeneID').verbose_name
        field_label6 = test_obj._meta.get_field('isTF').verbose_name
        field_label7 = test_obj._meta.get_field('strand').verbose_name
        field_label8 = test_obj._meta.get_field('annotationVersion_id').verbose_name
        field_labels = [field_label0, field_label1, field_label2, field_label3, field_label4, field_label5, field_label6, field_label7, field_label8]
        self.assertEquals(field_labels, ['chr', 'start', 'end', 'geneID', 'geneSymbol', 'alternativeGeneID', 'isTF', 'strand', 'annotationVersion'])

    def test_geneAnnotation_max_length(self):
        test_obj = geneAnnotation.objects.get(geneID='200gBrownSugar')
        max_length0 = test_obj._meta.get_field('chr').max_length
        max_length1 = test_obj._meta.get_field('geneID').max_length
        max_length2 = test_obj._meta.get_field('geneSymbol').max_length
        max_length3 = test_obj._meta.get_field('alternativeGeneID').max_length
        max_length4 = test_obj._meta.get_field('isTF').max_length
        max_length5 = test_obj._meta.get_field('strand').max_length
        max_lengths = [max_length0, max_length1, max_length2, max_length3, max_length4, max_length5]
        self.assertEquals(max_lengths, [10, 255, 255, 255, 255, 1])

    def test_geneAnnotation_string(self):  # also shows that all attributes were assigned correctly
        test_obj = geneAnnotation.objects.get(geneID='200gBrownSugar')
        expected_object_name = str(test_obj.geneID) + " " + str(test_obj.chr) + ":" + str(test_obj.start) + "-" + str(test_obj.end) + " "  + str(test_obj.geneSymbol) + " " + str(test_obj.isTF) + " " + str(test_obj.strand) + " " + str(test_obj.annotationVersion)
        self.assertEquals(expected_object_name, str(test_obj))


class REMAnnotationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # We first need the two other instances due to the foreign keys
        print('Model Test - REMAnnotation')
        genomeAnnotation.objects.create(annotationVersion='the', genomeVersion='best', databaseName='chocolate')
        geneAnnotation.objects.create(chr='250gButter', start=1, end=2, geneID='200gBrownSugar',
                                      geneSymbol='175gSugar', alternativeGeneID='2Eggs', isTF='375gFlour',
                                      strand='+', annotationVersion_id='the')
        REMAnnotation.objects.create(chr='200gNuts', start=1, end=2, geneID_id='200gBrownSugar', REMID='2TSBakingPowder', regressionCoefficient=1.0, pValue=0.0001, version=1)

    def test_REMAnnotation_label(self):
        test_obj = REMAnnotation.objects.get(REMID='2TSBakingPowder')
        field_label0 = test_obj._meta.get_field('chr').verbose_name
        field_label1 = test_obj._meta.get_field('start').verbose_name
        field_label2 = test_obj._meta.get_field('end').verbose_name
        field_label3 = test_obj._meta.get_field('geneID').verbose_name
        field_label4 = test_obj._meta.get_field('REMID').verbose_name
        field_label5 = test_obj._meta.get_field('regressionCoefficient').verbose_name
        field_label6 = test_obj._meta.get_field('pValue').verbose_name
        field_label7 = test_obj._meta.get_field('version').verbose_name
        field_labels = [field_label0, field_label1, field_label2, field_label3, field_label4, field_label5, field_label6, field_label7]
        self.assertEquals(field_labels, ['chr', 'start', 'end', 'geneID', 'REMID', 'regressionCoefficient', 'pValue', 'version'])

    def test_REMAnnotation_max_length(self):
        test_obj = REMAnnotation.objects.get(REMID='2TSBakingPowder')
        max_length0 = test_obj._meta.get_field('chr').max_length
        max_length1 = test_obj._meta.get_field('REMID').max_length
        max_length2 = test_obj._meta.get_field('version').max_length
        max_lengths = [max_length0, max_length1, max_length2]
        self.assertEquals(max_lengths, [10, 255, 1])

    def test_REMAnnotation_string(self):  # also shows that all attributes were assigned correctly
        test_obj = REMAnnotation.objects.get(REMID='2TSBakingPowder')
        expected_object_name = str(test_obj.REMID)  +  " " + str(test_obj.chr) + ":" + str(test_obj.start) + "-" + str(test_obj.end)
        self.assertEquals(expected_object_name, str(test_obj))


class sampleInfoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # We first need the two other instances due to the foreign keys
        print('Model Test - sampleInfo')
        cellTypes.objects.create(cellTypeID='chip', cellTypeName='cookies', cellOntologyTerm='ingredients:')
        sampleInfo.objects.create(sampleID='300gDarkChocolate', originalSampleID='Preparation:', cellTypeID_id='chip', origin='mixButterAndSugarFoamy', dataType='AddEggs')

    def test_sampleInfo_label(self):
        test_obj = sampleInfo.objects.get(sampleID='300gDarkChocolate')
        field_label0 = test_obj._meta.get_field('sampleID').verbose_name
        field_label1 = test_obj._meta.get_field('originalSampleID').verbose_name
        field_label2 = test_obj._meta.get_field('cellTypeID').verbose_name
        field_label3 = test_obj._meta.get_field('origin').verbose_name
        field_label4 = test_obj._meta.get_field('dataType').verbose_name
        field_labels = [field_label0, field_label1, field_label2, field_label3, field_label4]
        self.assertEquals(field_labels, ['sampleID', 'originalSampleID', 'cellTypeID', 'origin', 'dataType'])

    def test_sampleInfo_max_length(self):
        test_obj = sampleInfo.objects.get(sampleID='300gDarkChocolate')
        max_length0 = test_obj._meta.get_field('sampleID').max_length
        max_length1 = test_obj._meta.get_field('originalSampleID').max_length
        max_length2 = test_obj._meta.get_field('origin').max_length
        max_length3 = test_obj._meta.get_field('dataType').max_length
        max_lengths = [max_length0, max_length1, max_length2, max_length3]
        self.assertEquals(max_lengths, [255, 255, 255, 255])

    def test_sampleInfo_string(self):  # also shows that all attributes were assigned correctly
        test_obj = sampleInfo.objects.get(sampleID='300gDarkChocolate')
        expected_object_name = str(test_obj.sampleID) + " " + str(test_obj.originalSampleID) + " " + str(test_obj.cellTypeID) + " " + str(test_obj.origin) + " " + str(test_obj.dataType)
        self.assertEquals(expected_object_name, str(test_obj))


class geneExpressionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # We first need the two other instances due to the foreign keys
        print('Model Test - geneExpression')
        genomeAnnotation.objects.create(annotationVersion='the', genomeVersion='best',  databaseName='chocolate')
        geneAnnotation.objects.create(chr='250gButter', start=1, end=2, geneID='200gBrownSugar', geneSymbol='175gSugar', alternativeGeneID='2Eggs', isTF='375gFlour', strand='+', annotationVersion_id='the')
        cellTypes.objects.create(cellTypeID='chip', cellTypeName='cookies', cellOntologyTerm='ingredients:')
        sampleInfo.objects.create(sampleID='300gDarkChocolate', originalSampleID='Preparation:', cellTypeID_id='chip', origin='mixButterAndSugarFoamy', dataType='AddEggs')
        geneExpression.objects.create(geneID_id='200gBrownSugar', sampleID_id='300gDarkChocolate', expressionLog2TPM=1.0, species='AddFlourAndBakingPowder')

    def test_geneExpression_label(self):
        test_obj = geneExpression.objects.get(sampleID='300gDarkChocolate')
        field_label0 = test_obj._meta.get_field('geneID').verbose_name
        field_label1 = test_obj._meta.get_field('sampleID').verbose_name
        field_label2 = test_obj._meta.get_field('expressionLog2TPM').verbose_name
        field_label3 = test_obj._meta.get_field('species').verbose_name
        field_labels = [field_label0, field_label1, field_label2, field_label3]
        self.assertEquals(field_labels, ['geneID', 'sampleID', 'expressionLog2TPM', 'species'])

    def test_geneExpression_max_length(self):
        test_obj = geneExpression.objects.get(sampleID='300gDarkChocolate')
        max_length0 = test_obj._meta.get_field('species').max_length
        max_lengths = [max_length0]
        self.assertEquals(max_lengths, [255])

    def test_geneExpression_string(self):  # also shows that all attributes were assigned correctly
        test_obj = geneExpression.objects.get(sampleID='300gDarkChocolate')
        expected_object_name = str(test_obj.geneID) + ' ' + str(test_obj.sampleID) + ' ' + str(test_obj.expressionLog2TPM)

        self.assertEquals(expected_object_name, str(test_obj))


class REMActivityModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # We first need the two other instances due to the foreign keys
        print('Model Test - REMActivity')
        cellTypes.objects.create(cellTypeID='chip', cellTypeName='cookies', cellOntologyTerm='ingredients:')
        sampleInfo.objects.create(sampleID='300gDarkChocolate', originalSampleID='Preparation:',
                                  cellTypeID_id='chip', origin='mixButterAndSugarFoamy', dataType='AddEggs')
        genomeAnnotation.objects.create(annotationVersion='the', genomeVersion='best', databaseName='chocolate')
        geneAnnotation.objects.create(chr='250gButter', start=1, end=2, geneID='200gBrownSugar',
                                      geneSymbol='175gSugar', alternativeGeneID='2Eggs', isTF='375gFlour',
                                      strand='+', annotationVersion_id='the')
        REMAnnotation.objects.create(chr='200gNuts', start=1, end=2, geneID_id='200gBrownSugar', REMID='2TSBakingPowder', regressionCoefficient=1.0, pValue=0.0001, version=1)
        REMActivity.objects.create(REMID_id='2TSBakingPowder', sampleID_id='300gDarkChocolate', dnase1Log2=1.0, version=1)

    def test_REMActivity_label(self):
        test_obj = REMActivity.objects.get(sampleID='300gDarkChocolate')
        field_label0 = test_obj._meta.get_field('REMID').verbose_name
        field_label1 = test_obj._meta.get_field('sampleID').verbose_name
        field_label2 = test_obj._meta.get_field('dnase1Log2').verbose_name
        field_label3 = test_obj._meta.get_field('version').verbose_name
        field_labels = [field_label0, field_label1, field_label2, field_label3]
        self.assertEquals(field_labels, ['REMID', 'sampleID', 'dnase1Log2', 'version'])

    def test_REMActivity_string(self):  # also shows that all attributes were assigned correctly
        test_obj = REMActivity.objects.get(sampleID='300gDarkChocolate')
        expected_object_name = str(test_obj.REMID)
        self.assertEquals(expected_object_name, str(test_obj))


class CREMAnnotationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # We first need the two other instances due to the foreign keys
        print('Model Test - CREMAnnotation')
        genomeAnnotation.objects.create(annotationVersion='the', genomeVersion='best', databaseName='chocolate')
        geneAnnotation.objects.create(chr='250gButter', start=1, end=2, geneID='200gBrownSugar',
                                      geneSymbol='175gSugar', alternativeGeneID='2Eggs', isTF='375gFlour',
                                      strand='+', annotationVersion_id='the')
        REMAnnotation.objects.create(chr='200gNuts', start=1, end=2, geneID_id='200gBrownSugar', REMID='2TSBakingPowder', regressionCoefficient=1.0, pValue=0.0001, version=1)
        CREMAnnotation.objects.create(REMID_id='2TSBakingPowder', CREMID='MixWithChocolateAndNuts', chr='FormHeaps', start=1, end=2, REMsPerCREM=42, version=1)

    def test_CREMAnnotation_label(self):
        test_obj = CREMAnnotation.objects.get(CREMID='MixWithChocolateAndNuts')
        field_label0 = test_obj._meta.get_field('REMID').verbose_name
        field_label1 = test_obj._meta.get_field('CREMID').verbose_name
        field_label2 = test_obj._meta.get_field('chr').verbose_name
        field_label3 = test_obj._meta.get_field('start').verbose_name
        field_label4 = test_obj._meta.get_field('end').verbose_name
        field_label5 = test_obj._meta.get_field('REMsPerCREM').verbose_name
        field_label6 = test_obj._meta.get_field('version').verbose_name
        field_labels = [field_label0, field_label1, field_label2, field_label3, field_label4, field_label5, field_label6]
        self.assertEquals(field_labels, ['REMID', 'CREMID', 'chr', 'start', 'end', 'REMsPerCREM', 'version'])

    def test_CREMAnnotation_max_length(self):
        test_obj = CREMAnnotation.objects.get(CREMID='MixWithChocolateAndNuts')
        max_length0 = test_obj._meta.get_field('CREMID').max_length
        max_length1 = test_obj._meta.get_field('chr').max_length
        max_lengths = [max_length0, max_length1]
        self.assertEquals(max_lengths, [255, 10])

# Bake at 175 degrees Celsius 10 to 12 minutes. Let them cool. They should still be soft when taken out of the oven.
