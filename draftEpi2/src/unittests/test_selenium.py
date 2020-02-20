# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
#
# from table_manager.models import *
# from geneQuery.views import *
# from regionQuery.views import *
# from remQuery.views import *
#
#
#
#
# # Simple assignment
# from selenium.webdriver import Chrome
# # Chrome(executable_path='//Users//dennis//GitHub//EpiRegioDB//browser_drivers//chromedriver.exe')
# driver = webdriver.Chrome(executable_path='//Users//dennis//GitHub//EpiRegioDB//browser_drivers//chromedriver')
# driver.get('http://127.0.0.1:8000/REMQuery')  # open the website
#
# first_name = driver.find_element_by_id('REMIDs')
#
# submit = driver.find_element_by_id('QueryButton')
#
# # Fill the form with data
# first_name.send_keys('REM0000742')
#
# # submitting the form
# submit.send_keys(Keys.RETURN)
#
#
#
# class AccountTestCase(LiveServerTestCase):
#
#     def setUp(self):
#         self.selenium = webdriver.Firefox(executable_path='/Users/dennis/GitHub/EpiRegioDB/geckodriver-master/geckodriver.exe')
#         super(AccountTestCase, self).setUp()
#         genomeAnnotation.objects.create(genomeVersion='hg38', annotationVersion='V26', databaseName='gencode')
#         cellTypes.objects.create(cellTypeID='CTID_0000046', cellTypeName='muscle of leg',
#                                  cellOntologyTerm='UBERON:0001383')
#         sampleInfo.objects.create(sampleID='R_ENCBS011TVS', originalSampleID='ENCBS011TVS',
#                                   cellTypeID_id='CTID_0000046', origin='Roadmap', dataType=3)
#         # one geneAnnotation with a REM
#         geneAnnotation.objects.create(chr='chr1', start=826206, end=827522, geneID='ENSG00000225880',
#                                       geneSymbol='LINC00115', alternativeGeneID='', isTF='Unknown', strand='-',
#                                       annotationVersion_id='V26')
#         # one geneAnnotation without a REM, to test for valid genes we have no data for
#         geneAnnotation.objects.create(chr='chr1', start=826206, end=827522, geneID='ENSG00000XXXXXX',
#                                       geneSymbol='LINCXXXXX', alternativeGeneID='', isTF='Unknown', strand='-',
#                                       annotationVersion_id='V26')
#         REMAnnotation.objects.create(chr='chr1', start=827246, end=827445, geneID_id='ENSG00000225880',
#                                      REMID='REM0000742', regressionCoefficient=-0.0749712, pValue=0.75073,
#                                      version='1')
#         REMActivity.objects.create(REMID_id='REM0000742', sampleID_id='R_ENCBS011TVS', dnase1Log2=13.1186,
#                                    version='1')
#         geneExpression.objects.create(geneID_id='ENSG00000225880', sampleID_id='R_ENCBS011TVS',
#                                       expressionLog2TPM=0.265575, species='HUMAN')
#         CREMAnnotation.objects.create(REMID_id='REM0000742', CREMID='CREM0000464', chr='chr1', start=826308,
#                                       end=827500, REMsPerCREM=27, version=1)
#
#     def tearDown(self):
#         self.selenium.quit()
#         super(AccountTestCase, self).tearDown()
#
#     def test_register(self):
#         selenium = self.selenium
#         #Opening the link we want to test
#         selenium.get('http://127.0.0.1:8000/REMQuery/')
#         #find the form element
#         first_name = selenium.find_element_by_id('REMIDs')
#
#         submit = selenium.find_element_by_id('QueryButton')
#
#         #Fill the form with data
#         first_name.send_keys('REM0000742')
#
#         #submitting the form
#         submit.send_keys(Keys.RETURN)
#
#         #check the returned result
#         assert 'Check your email' in selenium.page_source