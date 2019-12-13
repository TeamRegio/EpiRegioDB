REST API
========

EpiRegioDB provides an user-friendly REST framework based web interface to retrieve information from our database. This browsable interface provides information as a JSON file.



General Information
-------------------

The REST API allows 3 different kinds of queries (GeneQuery, RegionQuery and REMQuery), which have similar functionalities as the corresponding queries of the web interface (Gene ID, Gene region and Regulatory element).
Furthermore, there is a query that reports all REMs that belong to a CREM (CREMQuery) and a query that provides general information of a gene (GeneInfo). 
All queries follow the same syntax rule::
        www.epiregio.de/REST_API/<query>/<input>/,
where *input* represents the input of the current query.
For instance, if you are interested in, which REMs are linked to the gene ENSG00000223972, then *query* is *GeneQuery* and *input* is *ENSG00000223972*, which results in the following url::
        `www.epiregio.de/REST_API/GeneQuery/ENSG00000223972/ <www.epiregio.de/REST_API/GeneQuery/ENSG00000223972/>`_.
In addition, it is possible to request information for multiple inputs within one run. 
Therefore, the inputs need to be separated by an underscore. Sticking with the previously example,:: 
        www.epiregio.de/REST_API/GeneQuery/ENSG00000223972_ENSG00000223973_ENSG00000223974/
returns all REMs associated to the genes ENSG00000223972 ENSG00000223973 and ENSG00000223974. 
The following provides more information as well as an example for each kind of query.

GeneQuery
----------------
This query return for an input gene (or multiple genes) given as ensembl id(s) the associated REMs. 
In detail the geneID, geneSymbol, REMID, chr, start, end, regressionCoefficient, p-value, version of the Epiregio database, number of REMs per CREM, CREM ID, and a list of  the log2(dnase1 signal) of the cell type used in STITCHIT are displayed.

**Example:**
Please have a look at the General Information section for an example.

RegionQuery
-----------
Given a genomic region, this query returns all overlapping REMs. 
The genomic region must be given as chr:start-end, where start is smaller or equal than end (e.g. chr16:75423948-75424405). 
The output has the same format as for the GeneQuery.

**Example:**::
        www.epiregio.de/REST_API/RegionQuery/chr16:75423948-75424405/

        www.epiregio.de/REST_API/RegionQuery/chr16:75423948-75424405_chr2:1369428-3456742/

REMQuery:
---------
This query answers the question, which gene is linked to a given REM. 
Therefore, the input must be a valid REM ID (e.g REM0000006).
As for the GeneQuery and the RegionQuery, multiple inputs are possible, and the output has the same format.

**Example:**::
        www.epiregio.de/REST_API/REMQuery/REM0000002/

        www.epiregio.de/REST_API/REMQuery/REM0000002_REM0000007/

CREAMQuery
----------
Given a CREM ID (e.g CREM0000007) or multiple CREM IDs (e.g CREM0000002_CREM0000008), this query lists all REMs of the CREM(s). 
The output format is the same as for the GeneQuery. 

Example:
~~~~~~~~
::
        www.epiregio.de/REST_API/CREMQuery/CREM0000002/

        www.epiregio.de/REST_API/CREMQuery/CREM0000002_CREM0000008/

GeneInfo
---------
Returns for a given ensembl ID or multiple ensembl ids general gene information such as chr, start, end, gene symbol, alternative gene id, strand, and annotation version. 

Example:
~~~~~~~
::
        www.epiregio.de/REST_API/GeneInfo/ENSG00000223972/
        www.epiregio.de/REST_API/GeneInfo/ENSG00000223972_ENSG00000223978/


