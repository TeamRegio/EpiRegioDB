REST API
========

EpiRegioDB provides an user-friendly REST framework based web interface to retrieve information from our database. This browsable interface provides information as a JSON file.



General Information
-------------------

The REST API allows 3 different kinds of queries (GeneQuery, RegionQuery and REMQuery), which have similar functionalities as the corresponding queries of the web interface (Gene ID, Genomic region and Regulatory element).
Furthermore, there is a query that reports all REMs that belong to a cluster of REMs (CREMQuery) and a query that provides general information of a gene (GeneInfo). 
All queries follow the same syntax rule::
        https://epiregio.de/REST_API/<query>/<input>/
where *input* represents the input of the current query.
For instance, if you are interested in which REMs are linked to the gene ENSG00000223972, then *query* is *GeneQuery* and *input* is *ENSG00000223972*, which results in the following URL:

        https://epiregio.de/REST_API/GeneQuery/ENSG00000223972/

In addition, it is possible to request information for multiple inputs within one run. 
Therefore, the inputs need to be separated by an underscore '_'. This can be done as follows 

        https://epiregio.de/REST_API/GeneQuery/ENSG00000223972_ENSG00000223974/

returns all REMs associated to the genes ENSG00000223972, and ENSG00000223974. 
The following provides more information as well as an example for each of the query types.

GeneQuery
----------------
Given an ensembl gene ID or gene symbol (or multiple ones) as input, this query returns the associated REMs.
In detail, the geneID, geneSymbol, REMID, chr, start, end, regressionCoefficient, p-value, version of the Epiregio database, number of REMs per CREM, CREM ID, and a list of the log2(dnase1 signal) of the cell type used in STITCHIT are displayed.

Example
~~~~~~~
Please have a look at the *General Information* section above for an example.

RegionQuery
-----------
Given a genomic region, this query returns all REMs that lie completely within this region. 
The genomic region must be given as chr:start-end, where start is smaller or equal than end (e.g. chr16:75423948-75424405). 
The output has the same format as the *GeneQuery* output. Optionally, you can also hand an overlap value to the URL like this: RegionQuery/50/... which retrieves all REMs that overlap with the regions by at least 50% of their length.

Example:
~~~~~~~
        https://epiregio.de/REST_API/RegionQuery/chr16:75423948-75424405/
        
        https://epiregio.de/REST_API/RegionQuery/50/chr16:75423948-75424405/
        
        https://epiregio.de/REST_API/RegionQuery/chr16:75423948-75424405_chr2:1369428-1369900/

REMQuery:
---------
This query answers the question, which gene is linked to a given REM. 
Therefore, the input must be a valid REM ID (e.g REM0000006).
As it was for the *GeneQuery* and the *RegionQuery* before, multiple inputs are possible, and the output has the same format.

Example:
~~~~~~~ 
        https://epiregio.de/REST_API/REMQuery/REM0000002/
        
        https://epiregio.de/REST_API/REMQuery/REM0000002_REM0000007_REM0000009/

CREMQuery
----------
Given a CREM ID (e.g CREM0000007) or multiple CREM IDs (e.g CREM0000002_CREM0000008), this query lists all REMs contained in the CREM(s). 
The output format is the same as for the *GeneQuery*. 

Example:
~~~~~~~~
        https://epiregio.de/REST_API/CREMQuery/CREM0000002/
        
        https://epiregio.de/REST_API/CREMQuery/CREM0000002_CREM0000008_CREM0000009/

GeneInfo
---------
For a given ensembl ID (or multiple ones), the query returns general gene information such as chr, start, end, gene symbol, alternative gene id, strand, and annotation version. 

Example:
~~~~~~~
        https://epiregio.de/REST_API/GeneInfo/ENSG00000223972/
        
        https://epiregio.de/REST_API/GeneInfo/ENSG00000223972_ENSG00000223978/



Programmatic access via Python
---------
If you wish to call the REST API outside of your browser, for example if you need to get data regularly and want to include it into one of your scripts, you need a program that is capable of doing HTTP requests. One easy-to-use tool is the Python package `Requests <https://requests.readthedocs.io/en/master/>`_. Let's go through an example: you have a Python list with genomic regions and you really want to know which REMs overlap by at least 50% with your regions. In the end, you want to have a new list, containing the REM IDs, their location as well as their cell type score for the left kidney. So here is what we need to get going::

        import requests

        important_regions = [['chr16', 75423948, 75424405], ['chr2', 1369428, 1369900], ['chr1', 8000, 25999]]
        overlap = 50
        important_results = []  # Let's already define our output

Requests is straightforward to use, pass an URL to the requests.get() function and proceed with it as you need it. In our case this could look like this::

        
        for region in important_regions:
                our_url = 'https://epiregio.de/REST_API/RegionQuery/'+str(overlap)+'/'+region[0]+':'+str(region[1])+'-'+str(region[2])+'/'
                api_call = requests.get(our_url)
                if api_call.status_code != 200:  # In case the page does not work properly.
                        print("Page Error")
                for hit in api_call.json():
                        important_results.append([hit['REMID'], hit['chr'], hit['start'], hit['end'], hit['cellTypeActivity']['left kidney']])

        
