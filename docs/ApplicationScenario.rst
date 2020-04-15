Application scenarios
---------
In this section we provide a step-by-step explanation of two application scenarios of EpiRegio. The two scenarios are similar to those in our paper 'EpiRegio: Analysis and retrieval of regulatory elements linked
to genes (TODO: add link). 


How to use EpiRegio to identify TF's target genes using ChIP-seq peak regions?
=================
TODO: add intro, and say that we show it examplary on ARID3A


**Step 1:** Downloaded the binding locations of the TF of interest for instance from the ENCODE database as a BED file. As an example, we use the ChIP-seq peaks of TF ARID3A with the Accession number ENCFF002CVL. Either click `here <https://www.encodeproject.org/files/ENCFF002CVL/>`_ to get the data from the encode webpage or download the data via::
  wget 'https://www.encodeproject.org/files/ENCFF002CVL/@@download/ENCFF002CVL.bed.gz'

**Step 2:** Use EpiRegios Region query to search for REMs overlapping at least by 50% with the TF-ChIP peaks 

**Step 3:** Click to ... perform a function enrichment analysis using g:Profiler with default parameters (TODO: in the paper it is not the defaul setting, do we use the defaul settings on the website?).



Application scenario 2: How to use EpiRegio to identify enriched TFs of a set of genes of interest
=================
TODO: add intro


