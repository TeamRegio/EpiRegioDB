Application scenarios
---------
In this section we provide a step-by-step explanation of two application scenarios of EpiRegio. The two scenarios are similar to those in our paper 'EpiRegio: Analysis and retrieval of regulatory elements linked
to genes (TODO: add link). 


How to use EpiRegio to identify TF's target genes using ChIP-seq peak regions?
================
The application scenario is based on the section *Elucidation of disease pathways directly from a TF-ChIP experiment* from our paper.  


**Step 1:** Downloaded the binding locations of the TF of interest for instance from the ENCODE database as a BED file. As an example, we use the ChIP-seq peaks of TF ARID3A with the Accession number ENCFF002CVL. Either click `here <https://www.encodeproject.org/files/ENCFF002CVL/>`_ to get the data from the ENCODE webpage or download it via::

  wget 'https://www.encodeproject.org/files/ENCFF002CVL/@@download/ENCFF002CVL.bed.gz'

**Step 2:** Use EpiRegio's  `Region query <https://epiregiodb.readthedocs.io/en/latest/UseCases.html#region-query>`_ to search for REMs overlapping at least by 50% with the TF-ChIP peaks. Go to https://epiregio.de/regionQuery/, click *choose File* and upload the ChIP-seq peaks from Step 1. Next to the upload field, you can see a option *Overlap percentage (optional)* to define the percentage the binding locations and the REMs should overlap. Type 50 in this field and click *Query Database*.
TODO: add screenshot where you see axactky this 

**Step 3:** Click ... to perform a function enrichment analysis using g:Profiler with default parameters 
TODO: in the paper it is not the defaul setting, do we use the defaul settings on the website?, add screenshot



Application scenario 2: How to use EpiRegio to identify enriched TFs of a set of genes of interest
=================
TODO: add intro


