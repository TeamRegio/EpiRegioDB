REST API
========

EpiRegioDB provides an user-friendly REST framework based web interface to retrieve information from our database. This browsable interface provides information as a JSON file.

The REST API allows 3 different kinds of queries (GeneQuery, RegionQuery and REMQuery), which have similar functionalities as the corresponding queries of the web interface (Gene ID, Gene region and Regulatory element).
Furthermore, there is a query that reports all REMs that belong to a CREM (CREMQuery) and a query that provides general information of a gene (GeneInfo). 
All queries follow the same syntax rule:
.. code-block::
   www.epiregio.de/REST_API/<query>/<input>/


