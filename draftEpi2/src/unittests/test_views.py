from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.template.response import TemplateResponse
# Create your tests here.
# acts like a dummy web browser that we can use to simulate GET and POST requests on a URL and observe the response

from table_manager.models import *
from geneQuery.views import *
from regionQuery.views import *
from remQuery.views import *


# ==========================================================================
# Base Pages View Test
# ==========================================================================


# As base page we consider every page except for the result table pages
class basePageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        print('View Test - Base Pages')

    def test_HomeView(self):  # when doing multiple asserts, in case of an error we only get reported
        # the first one
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')
        self.assertEqual(response.status_code, 200)

    # Tests the URL, which templates are loaded and whether the status is OK
    def test_HelpView(self):
        response = self.client.get('/help/')
        self.assertTemplateUsed(response, 'help.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')
        self.assertEqual(response.status_code, 200)

    def test_ContactView(self):
        response = self.client.get('/contact/')
        self.assertTemplateUsed(response, 'contact.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')
        self.assertEqual(response.status_code, 200)

    def test_RESTAPIHomeView(self):
        response = self.client.get('/REST_API/')
        self.assertTemplateUsed(response, 'REST_API_home.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')
        self.assertEqual(response.status_code, 200)

    def test_geneQueryView(self):
        response = self.client.get('/geneQuery/')
        self.assertTemplateUsed(response, 'geneQuery.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')
        self.assertEqual(response.status_code, 200)

    def test_regionQueryView(self):
        response = self.client.get('/regionQuery/')
        self.assertTemplateUsed(response, 'regionQuery.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')
        self.assertEqual(response.status_code, 200)

    def test_REMQueryView(self):
        response = self.client.get('/REMQuery/')
        self.assertTemplateUsed(response, 'remQuery.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')
        self.assertEqual(response.status_code, 200)

    def test_REST_API_TypoView(self):
        typo_list = ['GeneInfo', 'GeneQuery', 'RegionQuery', 'REMQuery', 'CREMQuery']
        for typo in typo_list:
            response = self.client.get('/REST_API/'+typo+'/')
            self.assertTemplateUsed(response, 'REST_API_error.html')
            self.assertTemplateUsed(response, 'navbar.html')
            self.assertTemplateUsed(response, 'footer.html')
            self.assertEqual(response.status_code, 200)


class geneQuerySearchTest(TestCase):
    @classmethod
    # To be really able to check for all of our functions we have to create one complete dataset. The test cases don't
    # make use of the actual database, but create a test database that is destroyed afterwards
    def setUpTestData(cls):
        genomeAnnotation.objects.create(genomeVersion='hg38', annotationVersion='V26', databaseName='gencode')
        cellTypes.objects.create(cellTypeID='CTID_0000046', cellTypeName='muscle of leg', cellOntologyTerm='UBERON:0001383')
        sampleInfo.objects.create(sampleID='R_ENCBS011TVS', originalSampleID='ENCBS011TVS', cellTypeID_id='CTID_0000046', origin='Roadmap', dataType=3)
        # one geneAnnotation with a REM
        geneAnnotation.objects.create(chr='chr1', start=826206, end=827522, geneID='ENSG00000225880', geneSymbol='LINC00115', alternativeGeneID='', isTF='Unknown', strand='-', annotationVersion_id='V26')
        # one geneAnnotation without a REM, to test for valid genes we have no data for
        geneAnnotation.objects.create(chr='chr1', start=826206, end=827522, geneID='ENSG00000XXXXXX', geneSymbol='LINCXXXXX', alternativeGeneID='', isTF='Unknown', strand='-', annotationVersion_id='V26')
        REMAnnotation.objects.create(chr='chr1', start=827246, end=827445, geneID_id='ENSG00000225880', REMID='REM0000742', regressionCoefficient=-0.0749712, pValue=0.75073, version='1')
        REMActivity.objects.create(REMID_id='REM0000742', sampleID_id='R_ENCBS011TVS', dnase1Log2=13.1186, version='1')
        geneExpression.objects.create(geneID_id='ENSG00000225880', sampleID_id='R_ENCBS011TVS', expressionLog2TPM=0.265575, species='HUMAN')
        CREMAnnotation.objects.create(REMID_id='REM0000742', CREMID='CREM0000464', chr='chr1', start=826308, end=827500, REMsPerCREM=27, version=1)
        print('View Test - Gene Query Search')

    # ==========================================================================
    # Gene Query - including CREM and gene Detail
    # ==========================================================================
    def test_gene_search_view_numeric(self):
        print('-- numeric')
        response = self.client.post('/geneQuery_search/', {
            'geneID_numeric': 'ENSG00000225880, ENSG00000XXXXXX, ENSGINVALID',
            'geneSymbol': '',
            'gene_format': 'id_format',
            'csvFile': '',
            'cellTypes': 'muscle of leg, ',  # whitespace and comma to match the format of the html page
            'activ_thresh': 0.0,
        })

        # check all the output we should get, based on our test data created above
        self.assertTemplateUsed(response, 'geneQuery_search.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')
        self.assertEqual(response.context['data'][0], {
            'chr': 'chr1',
            'start': 827246,
            'end': 827445,
            'geneID_id': 'ENSG00000225880',
            'REMID': 'REM0000742',
            'regressionCoefficient': -0.0749712,
            'pValue': 0.75073,
            'CREMID': 'CREM0000464',
            'modelScore': 0.413633959051203,
            'geneSymbol': 'LINC00115',
            'version': '1',
            'REMsPerCREM': 27,
            'muscle of leg_dnase1Log2': 13.1186,
            'muscle of leg_samplecount': 1
             })
        self.assertEqual(response.context['invalid_list'], ['ENSGINVALID'])
        self.assertEqual(response.context['no_data'], ['ENSG00000XXXXXX'])
        self.assertEqual(response.context['query_string'],' ENSG00000225880, ENSG00000XXXXXX, ENSGINVALID')
        self.assertEqual(response.context['activ_thresh'], 0.0)
        self.assertEqual(response.context['cell_types_string'], 'muscle of leg')
        self.assertEqual(response.context['cell_types_list'], ['muscle of leg'])
        self.assertEqual(response.context['cell_types_list_upper'], ['Muscle of leg'])
        self.assertEqual(response.context['error_msg'], '')
        self.assertEqual(response.context['export_string'], 'ENSG00000225880,ENSG00000XXXXXX,ENSGINVALID')


    def test_gene_search_view_symbolic(self):
        print('-- symbolic')
        response = self.client.post('/geneQuery_search/', {
            'geneID_numeric': '',
            'geneSymbol': 'LINC00115, LINCXXXXX, LINCINVALID',  # is the button field
            'gene_format': 'symbol_format',
            'csvFile': '',
            'cellTypes': 'muscle of leg, ',  # whitespace and comma to match the format of the html page
            'activ_thresh': 0.0,
        })

        # check all the output we should get, based on our test data created above
        self.assertTemplateUsed(response, 'geneQuery_search.html')
        self.assertEqual(response.context['data'][0], {
            'chr': 'chr1',
            'start': 827246,
            'end': 827445,
            'geneID_id': 'ENSG00000225880',
            'REMID': 'REM0000742',
            'regressionCoefficient': -0.0749712,
            'pValue': 0.75073,
            'CREMID': 'CREM0000464',
            'modelScore': 0.413633959051203,
            'geneSymbol': 'LINC00115',
            'version': '1',
            'REMsPerCREM': 27,
            'muscle of leg_dnase1Log2': 13.1186,
            'muscle of leg_samplecount': 1,
        })
        self.assertEqual(response.context['invalid_list'], ['LINCINVALID'])
        self.assertEqual(response.context['no_data'], ['LINCXXXXX'])
        self.assertEqual(response.context['query_string'], ' LINC00115, LINCXXXXX, LINCINVALID')
        self.assertEqual(response.context['activ_thresh'], 0.0)
        self.assertEqual(response.context['cell_types_string'], 'muscle of leg')
        self.assertEqual(response.context['cell_types_list'], ['muscle of leg'])
        self.assertEqual(response.context['cell_types_list_upper'], ['Muscle of leg'])
        self.assertEqual(response.context['error_msg'], '')
        self.assertEqual(response.context['export_string'], 'LINC00115,LINCXXXXX,LINCINVALID')


    def test_gene_search_view_numeric_csv(self):
        print('-- numeric - csv upload')
        response = self.client.post('/geneQuery_search/', {
            'geneID_numeric': '',
            'geneSymbol': '',  # is the button field
            'gene_format': 'id_format',
            'csvFile': 'ENSG00000225880,ENSG00000XXXXXX,ENSGINVALID,',
            'cellTypes': 'muscle of leg, ',  # whitespace and comma to match the format of the html page
            'activ_thresh': 0.0,
        })

        # check all the output we should get, based on our test data created above
        self.assertTemplateUsed(response, 'geneQuery_search.html')
        self.assertEqual(response.context['data'][0], {
            'chr': 'chr1',
            'start': 827246,
            'end': 827445,
            'geneID_id': 'ENSG00000225880',
            'REMID': 'REM0000742',
            'regressionCoefficient': -0.0749712,
            'pValue': 0.75073,
            'CREMID': 'CREM0000464',
            'modelScore': 0.413633959051203,
            'geneSymbol': 'LINC00115',
            'version': '1',
            'REMsPerCREM': 27,
            'muscle of leg_dnase1Log2': 13.1186,
            'muscle of leg_samplecount': 1
             })
        self.assertEqual(response.context['invalid_list'], ['ENSGINVALID'])
        self.assertEqual(response.context['no_data'], ['ENSG00000XXXXXX'])
        self.assertEqual(response.context['query_string'],' ENSG00000225880, ENSG00000XXXXXX, ENSGINVALID')
        self.assertEqual(response.context['activ_thresh'], 0.0)
        self.assertEqual(response.context['cell_types_string'], 'muscle of leg')
        self.assertEqual(response.context['cell_types_list'], ['muscle of leg'])
        self.assertEqual(response.context['cell_types_list_upper'], ['Muscle of leg'])
        self.assertEqual(response.context['error_msg'], '')
        self.assertEqual(response.context['export_string'], 'ENSG00000225880,ENSG00000XXXXXX,ENSGINVALID')


    def test_gene_search_view_symbolic_csv(self):
        print('-- symbolic - csv upload')
        response = self.client.post('/geneQuery_search/', {
            'geneID_numeric': '',
            'geneSymbol': '',  # is the button field
            'gene_format': 'symbol_format',
            'csvFile': 'LINC00115,LINCXXXXX,LINCINVALID',
            'cellTypes': 'muscle of leg, ',  # whitespace and comma to match the format of the html page
            'activ_thresh': 0.0,
        })

        # check all the output we should get, based on our test data created above
        self.assertTemplateUsed(response, 'geneQuery_search.html')
        self.assertEqual(response.context['data'][0], {
            'chr': 'chr1',
            'start': 827246,
            'end': 827445,
            'geneID_id': 'ENSG00000225880',
            'REMID': 'REM0000742',
            'regressionCoefficient': -0.0749712,
            'pValue': 0.75073,
            'CREMID': 'CREM0000464',
            'modelScore': 0.413633959051203,
            'geneSymbol': 'LINC00115',
            'version': '1',
            'REMsPerCREM': 27,
            'muscle of leg_dnase1Log2': 13.1186,
            'muscle of leg_samplecount': 1,
        })
        self.assertEqual(response.context['invalid_list'], ['LINCINVALID'])
        self.assertEqual(response.context['no_data'], ['LINCXXXXX'])
        self.assertEqual(response.context['query_string'], ' LINC00115, LINCXXXXX, LINCINVALID')
        self.assertEqual(response.context['activ_thresh'], 0.0)
        self.assertEqual(response.context['cell_types_string'], 'muscle of leg')
        self.assertEqual(response.context['cell_types_list'], ['muscle of leg'])
        self.assertEqual(response.context['cell_types_list_upper'], ['Muscle of leg'])
        self.assertEqual(response.context['error_msg'], '')
        self.assertEqual(response.context['export_string'], 'LINC00115,LINCXXXXX,LINCINVALID')


    def test_gene_search_view_empty_data(self):
        print('-- empty data')
        response = self.client.post('/geneQuery_search/', {
            'geneID_numeric': '',
            'geneSymbol': '',  # is the button field
            'gene_format': 'symbol_format',
            'csvFile': 'LINCXXXXX,LINCINVALID',
            'cellTypes': 'muscle of leg, ',  # whitespace and comma to match the format of the html page
            'activ_thresh': 0.0,
        })
        # check all the output we should get, based on our test data created above
        self.assertTemplateUsed(response, 'empty_data.html')
        self.assertEqual(response.context['data'], [])
        self.assertEqual(response.context['invalid_list'], ['LINCINVALID'])
        self.assertEqual(response.context['no_data'], ['LINCXXXXX'])
        self.assertEqual(response.context['query_string'], ' LINCXXXXX, LINCINVALID')
        self.assertEqual(response.context['activ_thresh'], 0.0)
        self.assertEqual(response.context['cell_types_string'], 'muscle of leg')
        self.assertEqual(response.context['cell_types_list'], ['muscle of leg'])
        self.assertEqual(response.context['cell_types_list_upper'], ['Muscle of leg'])
        self.assertEqual(response.context['error_msg'], 'The model did not find putative REMs that are associated with your queried genes.')
        self.assertEqual(response.context['export_string'], 'LINCXXXXX,LINCINVALID')

    # when clicking on the query string, to provide more details on the genes
    def test_gene_detail_view_numeric(self):
        print('View Test - Gene Details numeric')
        response = self.client.get('/geneQuery_search/ ENSG00000225880/')
        self.assertTemplateUsed(response, 'gene_details.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')
        self.assertEqual(response.context['data'][0], {
            'chr': 'chr1',
            'start': 826206,
            'end': 827522,
            'geneID': 'ENSG00000225880',
            'geneSymbol': 'LINC00115',
            'alternativeGeneID': '',
            'isTF': 'Unknown',
            'strand': '-',
            'annotationVersion_id': 'V26',
        })
        self.assertEqual(response.context['query_list'], ['ENSG00000225880'])
        self.assertEqual(response.context['query_string'], ' ENSG00000225880')
        self.assertEqual(response.context['query_list_list'], ['ENSG00000225880'])
        self.assertEqual(response.context['export_string'], ' ENSG00000225880')

    def test_gene_detail_view_symbolic(self):
        print('View Test - Gene Details symbolic')
        response = self.client.get('/geneQuery_search/ LINC00115/')
        self.assertTemplateUsed(response, 'gene_details.html')
        self.assertEqual(response.context['data'][0], {
            'chr': 'chr1',
            'start': 826206,
            'end': 827522,
            'geneID': 'ENSG00000225880',
            'geneSymbol': 'LINC00115',
            'alternativeGeneID': '',
            'isTF': 'Unknown',
            'strand': '-',
            'annotationVersion_id': 'V26',
        })
        self.assertEqual(response.context['query_list'], ['ENSG00000225880'])
        self.assertEqual(response.context['query_string'], ' LINC00115')
        self.assertEqual(response.context['query_list_list'], ['LINC00115'])
        self.assertEqual(response.context['export_string'], ' LINC00115')


    def test_crem_view(self):
        print('View Test - CREM')
        response = self.client.get('/cluster/CREM0000464/')
        self.assertTemplateUsed(response, 'linked_crem.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')
        self.assertEqual(response.context['data'][0], {
            'REMID_id': 'REM0000742',
            'CREMID': 'CREM0000464',
            'chr': 'chr1',
            'start': 826308,
            'end': 827500,
            'REMsPerCREM': 27,
            'version': 1,
            'REMID_id__geneID': 'ENSG00000225880',
            'REMID_id__start': 827246,
            'REMID_id__end': 827445,
            'REMID_id__regressionCoefficient': -0.0749712,
            'REMID_id__pValue': 0.75073,
            'modelScore': 0.413633959051203
        })
        self.assertEqual(response.context['query'], 'CREM0000464')

    # ==========================================================================
    # Region Query
    # ==========================================================================
    def test_region_search_view(self):
        print('Test Views - Region search')
        response = self.client.post('/regionQuery_search/', {
            'geneRegions': 'chr1:816308-837500, chr2:1369428-2056742, Peter:Hans-Jürgen, ',
            'csvFile': '',
            'cellTypes': 'muscle of leg, ',  # whitespace and comma to match the format of the html page
            'activ_thresh': 0.0,
            'csv_upload': '',
            'csvFileRows': '',
        })
        # check all the output we should get, based on our test data created above
        self.assertTemplateUsed(response, 'regionQuery_search.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')
        self.assertEqual(response.context['data'][0], {
            'chr': 'chr1',
            'start': 827246,
            'end': 827445,
            'geneID_id': 'ENSG00000225880',
            'REMID': 'REM0000742',
            'regressionCoefficient': -0.0749712,
            'pValue': 0.75073,
            'version': '1',
            'REMsPerCREM': 27,
            'CREMID': 'CREM0000464',
            'geneSymbol': 'LINC00115',
            'muscle of leg_dnase1Log2': 13.1186,
            'muscle of leg_samplecount': 1,
            'modelScore': 0.413633959051203
        })
        self.assertEqual(response.context['invalid_list'], ['Peter:Hans-Jürgen'])
        self.assertEqual(response.context['no_data'], ['chr2:1369428-2056742'])
        self.assertEqual(response.context['query_string'], 'chr1:816308-837500, chr2:1369428-2056742, Peter:Hans-Jürgen')
        self.assertEqual(response.context['activ_thresh'], 0.0)
        self.assertEqual(response.context['cell_types_string'], 'muscle of leg')
        self.assertEqual(response.context['cell_types_list'], ['muscle of leg'])
        self.assertEqual(response.context['cell_types_list_upper'], ['Muscle of leg'])
        self.assertEqual(response.context['error_msg'], '')
        self.assertEqual(response.context['export_string'], 'chr1-816308-837500,chr2-1369428-2056742,Peter-Hans-Jürgen')


    def test_region_search_view_upload(self):
        print('-- upload')
        response = self.client.post('/regionQuery_search/', {
            'geneRegions': '',
            'csvFile': 'chr1, 816308, , 837500, chr2, 1369428, 2056742,, Hildegard, Jutta, Brunhilde ',
            'cellTypes': 'muscle of leg, ',  # whitespace and comma to match the format of the html page
            'activ_thresh': 0.0,
            'csv_upload': 'TestWritingIsSuperFun!.csv',
            'csvFileRows': '3',
        })
        # check all the output we should get, based on our test data created above
        self.assertTemplateUsed(response, 'regionQuery_search.html')
        self.assertEqual(response.context['data'][0], {
            'chr': 'chr1',
            'start': 827246,
            'end': 827445,
            'geneID_id': 'ENSG00000225880',
            'REMID': 'REM0000742',
            'regressionCoefficient': -0.0749712,
            'pValue': 0.75073,
            'version': '1',
            'REMsPerCREM': 27,
            'CREMID': 'CREM0000464',
            'geneSymbol': 'LINC00115',
            'muscle of leg_dnase1Log2': 13.1186,
            'muscle of leg_samplecount': 1,
            'modelScore': 0.413633959051203
        })
        self.assertEqual(response.context['invalid_list'], ['chrhildegard:Jutta-Brunhilde'])
        self.assertEqual(response.context['no_data'], ['chr2:1369428-2056742'])
        self.assertEqual(response.context['query_string'], 'chr1:816308-837500, chr2:1369428-2056742, chrhildegard:Jutta-Brunhilde')
        self.assertEqual(response.context['activ_thresh'], 0.0)
        self.assertEqual(response.context['cell_types_string'], 'muscle of leg')
        self.assertEqual(response.context['cell_types_list'], ['muscle of leg'])
        self.assertEqual(response.context['cell_types_list_upper'], ['Muscle of leg'])
        self.assertEqual(response.context['error_msg'], '')
        self.assertEqual(response.context['export_string'], 'chr1-816308-837500,chr2-1369428-2056742,chrhildegard-Jutta-Brunhilde')


    def test_region_search_view_empty(self):
        print('-- empty')
        response = self.client.post('/regionQuery_search/', {
            'geneRegions': 'chr2:1369428-2056742, Peter:Hans-Jürgen, ',
            'csvFile': '',
            'cellTypes': 'muscle of leg, ',  # whitespace and comma to match the format of the html page
            'activ_thresh': 0.0,
            'csv_upload': '',
            'csvFileRows': '',
        })
        # check all the output we should get, based on our test data created above
        self.assertTemplateUsed(response, 'empty_data.html')
        self.assertEqual(response.context['data'], [])
        self.assertEqual(response.context['invalid_list'], ['Peter:Hans-Jürgen'])
        self.assertEqual(response.context['no_data'], ['chr2:1369428-2056742'])
        self.assertEqual(response.context['query_string'], 'chr2:1369428-2056742, Peter:Hans-Jürgen')
        self.assertEqual(response.context['activ_thresh'], 0.0)
        self.assertEqual(response.context['cell_types_string'], 'muscle of leg')
        self.assertEqual(response.context['cell_types_list'], ['muscle of leg'])
        self.assertEqual(response.context['cell_types_list_upper'], ['Muscle of leg'])
        self.assertEqual(response.context['error_msg'], 'No REMs were found in your selected regions. You might want to try changing the region boundaries.')
        self.assertEqual(response.context['export_string'], 'chr2-1369428-2056742,Peter-Hans-Jürgen')

    # ==========================================================================
    # REM Query
    # ==========================================================================

    def test_REM_search_view(self):
        print('Test Views - REM search')
        response = self.client.post('/REMQuery_search/', {
            'REMIDs': 'REM0000742, Schaqueliene, ',
            'csvFile': '',
            'cellTypes': 'muscle of leg, ',  # whitespace and comma to match the format of the html page
            'activ_thresh': 0.0,
        })
        # check all the output we should get, based on our test data created above
        self.assertTemplateUsed(response, 'remQuery_search.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')
        self.assertEqual(response.context['data'][0], {
            'chr': 'chr1',
            'start': 827246,
            'end': 827445,
            'geneID_id': 'ENSG00000225880',
            'REMID': 'REM0000742',
            'regressionCoefficient': -0.0749712,
            'pValue': 0.75073,
            'version': '1',
            'REMsPerCREM': 27,
            'CREMID': 'CREM0000464',
            'geneSymbol': 'LINC00115',
            'muscle of leg_dnase1Log2': 13.1186,
            'muscle of leg_samplecount': 1,
            'modelScore': 0.413633959051203
        })
        self.assertEqual(response.context['invalid_list'], ['SCHAQUELIENE'])
        self.assertEqual(response.context['query_string'], ' REM0000742, SCHAQUELIENE')
        self.assertEqual(response.context['activ_thresh'], 0.0)
        self.assertEqual(response.context['cell_types_string'], 'muscle of leg')
        self.assertEqual(response.context['cell_types_list'], ['muscle of leg'])
        self.assertEqual(response.context['cell_types_list_upper'], ['Muscle of leg'])
        self.assertEqual(response.context['error_msg'], '')
        self.assertEqual(response.context['export_string'], 'REM0000742,SCHAQUELIENE')

    def test_REM_search_view_upload(self):
        print('-- upload')
        response = self.client.post('/REMQuery_search/', {
            'REMIDs': '',
            'csvFile': 'REM0000742, Schaqueliene, ',
            'cellTypes': 'muscle of leg, ',  # whitespace and comma to match the format of the html page
            'activ_thresh': 0.0,
        })
        # check all the output we should get, based on our test data created above
        self.assertTemplateUsed(response, 'remQuery_search.html')
        self.assertEqual(response.context['data'][0], {
            'chr': 'chr1',
            'start': 827246,
            'end': 827445,
            'geneID_id': 'ENSG00000225880',
            'REMID': 'REM0000742',
            'regressionCoefficient': -0.0749712,
            'pValue': 0.75073,
            'version': '1',
            'REMsPerCREM': 27,
            'CREMID': 'CREM0000464',
            'geneSymbol': 'LINC00115',
            'muscle of leg_dnase1Log2': 13.1186,
            'muscle of leg_samplecount': 1,
            'modelScore': 0.413633959051203
        })
        self.assertEqual(response.context['invalid_list'], ['SCHAQUELIENE'])
        self.assertEqual(response.context['query_string'], ' REM0000742, SCHAQUELIENE')
        self.assertEqual(response.context['activ_thresh'], 0.0)
        self.assertEqual(response.context['cell_types_string'], 'muscle of leg')
        self.assertEqual(response.context['cell_types_list'], ['muscle of leg'])
        self.assertEqual(response.context['cell_types_list_upper'], ['Muscle of leg'])
        self.assertEqual(response.context['error_msg'], '')
        self.assertEqual(response.context['export_string'], 'REM0000742,SCHAQUELIENE')

    def test_REM_search_view_empty(self):
        print('-- empty')
        response = self.client.post('/REMQuery_search/', {
            'REMIDs': 'MakePizzaGreatAgain, ChocolateSaladBestSalad',
            'csvFile': '',
            'cellTypes': 'muscle of leg, ',  # whitespace and comma to match the format of the html page
            'activ_thresh': 0.0,
        })
        # check all the output we should get, based on our test data created above
        self.assertTemplateUsed(response, 'empty_data.html')
        self.assertEqual(response.context['data'], [])
        for i in response.context['invalid_list']:
            self.assertIn(i, ['MAKEPIZZAGREATAGAIN', 'CHOCOLATESALADBESTSALAD'])
        self.assertEqual(response.context['query_string'], ' MAKEPIZZAGREATAGAIN, CHOCOLATESALADBESTSALAD')
        self.assertEqual(response.context['activ_thresh'], 0.0)
        self.assertEqual(response.context['cell_types_string'], 'muscle of leg')
        self.assertEqual(response.context['cell_types_list'], ['muscle of leg'])
        self.assertEqual(response.context['cell_types_list_upper'], ['Muscle of leg'])
        self.assertEqual(response.context['error_msg'], 'No REMs were found that match your query settings.')
        self.assertEqual(response.context['export_string'], 'MAKEPIZZAGREATAGAIN,CHOCOLATESALADBESTSALAD')

    # ==========================================================================
    # Ajax lookup
    # ==========================================================================
    def test_ajax_geneSymbols(self):
        print('Ajax - Gene Symbols')
        response = self.client.post('/genesymbol_search', {'search_text_gene': 'linc'})
        self.assertTemplateUsed(response, 'ajax_search_genesymbol.html')
        self.assertEqual(response.context['geneSymbol_search'], [('LINC00115',)])
        self.assertEqual(response.context['search_text_len'], 4)

    def test_ajax_geneSymbols_empty(self):
        print('-- empty')
        response = self.client.post('/genesymbol_search', {'search_text_gene': 'Ulrike'})
        self.assertTemplateUsed(response, 'ajax_search_genesymbol.html')
        self.assertEqual(response.context['geneSymbol_search'], [])
        self.assertEqual(response.context['search_text_len'], 6)

    def test_ajax_cellTypes(self):
        print('Ajax - Cell Types')
        response = self.client.post('/celltype_search', {'search_text': 'mu'})
        self.assertTemplateUsed(response, 'ajax_search_celltypes.html')
        self.assertEqual(response.context['cellType_search'], [('CTID_0000046', 'muscle of leg')])
        self.assertEqual(response.context['search_text_len'], 2)

    def test_ajax_cellTypes_empty(self):
        print('-- empty')
        response = self.client.post('/celltype_search', {'search_text': 'BigBrain'})
        self.assertTemplateUsed(response, 'ajax_search_celltypes.html')
        self.assertEqual(response.context['cellType_search'], [])
        self.assertEqual(response.context['search_text_len'], 8)


