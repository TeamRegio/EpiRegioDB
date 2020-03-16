from django.test import TestCase

# Create your tests here.
# acts like a dummy web browser that we can use to simulate GET and POST requests on a URL and observe the response

from table_manager.models import *
from geneQuery.views import *
from regionQuery.views import *
from remQuery.views import *
from API import *
from REST_API.views import *
from REST_API.serializers import *
from rest_framework.test import APITestCase

class CREMAnnotationModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # We first need the two other instances due to the foreign keys
        genomeAnnotation.objects.create(genomeVersion='hg38', annotationVersion='V26', databaseName='gencode')
        cellTypes.objects.create(cellTypeID='CTID_0000046', cellTypeName='muscle of leg', cellOntologyTerm='UBERON:0001383')
        sampleInfo.objects.create(sampleID='R_ENCBS011TVS', originalSampleID='ENCBS011TVS', cellTypeID_id='CTID_0000046', origin='Roadmap', dataType=3)
        # one geneAnnotation with a REM
        geneAnnotation.objects.create(chr='chr1', start=826206, end=827522, geneID='ENSG00000225880', geneSymbol='LINC00115', alternativeGeneID='', isTF='Unknown', strand='-', annotationVersion_id='V26')
        # one geneAnnotation without a REM, to test for valid genes we have no data for
        geneAnnotation.objects.create(chr='chr1', start=826206, end=827522, geneID='ENSG00000XXXXXX', geneSymbol='LINCXXXXX', alternativeGeneID='', isTF='Unknown', strand='-', annotationVersion_id='V26')
        REMAnnotation.objects.create(chr='chr1', start=827246, end=827445, geneID_id='ENSG00000225880', REMID='REM0000742', regressionCoefficient=-0.0749712, pValue=0.75073, version=1)
        REMActivity.objects.create(REMID_id='REM0000742', sampleID_id='R_ENCBS011TVS', dnase1Log2=13.1186, version=1)
        geneExpression.objects.create(geneID_id='ENSG00000225880', sampleID_id='R_ENCBS011TVS', expressionLog2TPM=0.265575, species='HUMAN')
        CREMAnnotation.objects.create(REMID_id='REM0000742', CREMID='CREM0000464', chr='chr1', start=826308, end=827500, REMsPerCREM=27, version=1)

    def test_API_geneQuery(self):
        print('API - Gene Query')
        response = self.client.get('/REST_API/GeneQuery/ENSG00000225880/')
        response.render()
        self.assertEqual(response.content, b'[{"geneID":"ENSG00000225880","geneSymbol":"LINC00115","REMID":"REM0000742","chr":"chr1","start":827246,"end":827445,"regressionCoefficient":-0.0749712,"pValue":0.75073,"version":1,"REMsPerCREM":27,"CREMID":"CREM0000464","modelScore":0.413633959051203,"cellTypeScore":{"muscle of leg":0.9835171843200001},"cellTypeActivity":{"muscle of leg":13.1186}}]')
        self.assertEqual(response.status_code, 200)

    def test_API_geneInfo(self):
        print('API - Gene Info')
        response = self.client.get('/REST_API/GeneInfo/ENSG00000225880/')
        response.render()
        # print(response.content)
        self.assertEqual(response.content, b'[{"geneID":"ENSG00000225880","chr":"chr1","start":826206,"end":827522,"geneSymbol":"LINC00115","alternativeGeneID":"","strand":"-","annotationVersion":"V26"}]')
        self.assertEqual(response.status_code, 200)

    def test_API_REMQuery(self):
        print('API - REM Query')
        response = self.client.get('/REST_API/REMQuery/REM0000742/')
        response.render()
        # print(response.content)
        self.assertEqual(response.content, b'[{"REMID":"REM0000742","chr":"chr1","start":827246,"end":827445,"geneID":"ENSG00000225880","geneSymbol":"LINC00115","regressionCoefficient":-0.0749712,"pValue":0.75073,"modelScore":0.413633959051203,"version":1,"REMsPerCREM":27,"CREMID":"CREM0000464","cellTypeScore":{"muscle of leg":0.9835171843200001},"cellTypeActivity":{"muscle of leg":13.1186}}]')
        self.assertEqual(response.status_code, 200)

    def test_API_CREMQuery(self):
        print('API - CREM Query')
        response = self.client.get('/REST_API/CREMQuery/CREM0000464/')
        response.render()
        # print(response.content)
        self.assertEqual(response.content, b'[{"CREMID":"CREM0000464","chr":"chr1","start":826308,"end":827500,"REMsPerCREM":27,"REMID":"REM0000742","linkedGene":"ENSG00000225880","REM_Start":827246,"REM_End":827445,"REM_RegressionCoefficient":-0.0749712,"REM_Pvalue":0.75073,"version":1}]')
        self.assertEqual(response.status_code, 200)

    def test_API_RegionQuery(self):
        print('API - Region Query')
        response = self.client.get('/REST_API/RegionQuery/chr1:827246-827445/')
        response.render()
        # print(response.content)
        self.assertEqual(response.content, b'[{"geneID":"ENSG00000225880","geneSymbol":"LINC00115","REMID":"REM0000742","chr":"chr1","start":827246,"end":827445,"regressionCoefficient":-0.0749712,"pValue":0.75073,"modelScore":0.413633959051203,"version":1,"REMsPerCREM":27,"CREMID":"CREM0000464","cellTypeScore":{"muscle of leg":0.9835171843200001},"cellTypeActivity":{"muscle of leg":13.1186}}]')
        self.assertEqual(response.status_code, 200)

