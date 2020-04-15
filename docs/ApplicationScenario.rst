Application scenarios
---------
In this section we provide a step-by-step explanation of two application scenarios of EpiRegio. The two scenarios are similar to those in our paper *EpiRegio: Analysis and retrieval of regulatory elements linked to genes* (TODO: add link). 


How to use EpiRegio to identify TF's target genes using ChIP-seq peak regions?
================
The application scenario is based on the section *Elucidation of disease pathways directly from a TF-ChIP experiment* from our paper. 


**Step 1:** Downloaded the binding locations of the TF of interest, for instance from the ENCODE database as a BED file. As an example, we use the ChIP-seq peaks of TF ARID3A with the accession number ENCFF002CVL. Either click `here <https://www.encodeproject.org/files/ENCFF002CVL/>`_ to get the data from the ENCODE webpage or download it via::

  wget 'https://www.encodeproject.org/files/ENCFF002CVL/@@download/ENCFF002CVL.bed.gz'.
  
 Unzip the file using e.g.::
 
    gzip -d ENCFF002CVL.bed.gz 

**Step 2:** Use EpiRegio's  `Region Query <https://epiregiodb.readthedocs.io/en/latest/UseCases.html#region-query>`_ to search for REMs overlapping at least by 50% with the TF-ChIP peaks. Go to https://epiregio.de/regionQuery/, click *choose File* and upload the ChIP-seq peaks from Step 1. Next to the upload field, you can see a option *Overlap percentage (optional)* to define the percentage the binding locations and the REMs should overlap. Since we want a 50% overlap, type 50 in this field and click *Query Database*. 
TODO: add screenshot where you see exactly this 

**Step 3:** Click the bottom *Functional enrichment analysis g:Profiler* in the upper left corner, to perform a GO term enrichment analysis using g:Profiler (default parameters) of the resulting REMs.  
TODO: add screenshot


How to use EpiRegio to identify enriched TFs of a set of genes of interest
=================
The application scenario is based on the section *Identify enriched transcription factors of differentially expressed genes* from our paper. To perform the analysis the motif enrichment tool `PASTAA <http://trap.molgen.mpg.de/PASTAA/>`_  and `bedtools <https://bedtools.readthedocs.io/en/latest/content/installation.html>`_ must be installed on your machine.
TODO: provide TRAP script with normalization on GitHub page

**Step 1:**  As an example, we consider a set of differential expressed genes based on a single-cell RNAseq
data set from Glaser et al. (cite), where Human Umbilical Endothelial Cells (HUVECs) were treated with TGF-beta to trigger an endothelial-to-mesenchymal transition (EndoMT). However the analysis works with every set of genes. If you want to perform the example you can download the differential expressed genes from our GitHub repository (link).

**Step 2:** Use EpiRegio's `Gene Query <https://epiregiodb.readthedocs.io/en/latest/UseCases.html#query-guide>`_ to identify the REMs assoiacted to the genes of interest. Go to https://epiregio.de/geneQuery/, click *choose File* and upload the file from Step 1. Enter *heart* to the field *Filter for cell types/tissues:*. We are interested on the regulatory effect of the tissue heart because endothelial cells within the heart undergo EndoMT during cardiac development. If your are using an individual data set, please also choose a celltype or tissue which is most suitable for your data. Next click *Query Database*. TODO: add screenshot

**Step 3:**   To apply *PASTAA*, we need a ranking of the resulting REMs. Therefore, we sort them in descending order based on the column *heart score*. To do so, click on the arrows next to *heart score*. Download the resulting table by clicking on the bottom *CSV*. TODO: add screenshot

**Step 4:** Next we determine the DNA-sequence of the identified REMs using *bedtools* and then run *PASTAA* to perform the motif enrichment analysis. On our GitHub repository we provide a workflow to run the analysis. Download the folder ... (link).
There we also provide a set of TF binding motifs downloaded from the JASPAR database (version 2020). To run the workflow, enter the following command to our consol:: 

  bash workflow.sh <pathToMotifs> <pathToPASTAA> <pathToBedtools> <REMs> <outputDir> <pvalue>



pvalue 0:05

How to use EpiRegio to identify TF binding sites within REMs of a gene of interest
=================
this is not a application scenario from the paper

**Step 1:** Gene Query
**Step 2:** bedtools getFasta
**Step 3:** use fimo, provide JASPAR motifs in meme format

