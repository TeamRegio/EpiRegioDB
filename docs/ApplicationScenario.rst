Application scenarios
---------
In this section we provide a step-by-step explanation of two application scenarios of EpiRegio. The two scenarios are introduced in more detail in our paper 'EpiRegio: Analysis and retrieval of regulatory elements linked
to genes' (TODO: add link). 


Application scenario 1: How to identify TF's target genes using ChIP-seq peak regions?
=================
We downloaded the binding locations of the TF ARID3A from
the ENCODE database (Accession: ENCFF002CVL) as a
BED file which contained 9,026 TF-ChIP peaks. We searched
for REMs overlapping at least by 50% with the TF-ChIP
peaks using the Region query in the EPIREGIO webserver.
The resulting REMs were associated with 1;730 unique genes.
We subjected them to a functional enrichment analysis using
g:Profiler (29) with default parameters, except setting the
significance threshold to 0:05 using the Benjamini-Hochberg
FDR method. The g:Profiler analysis can be reproduced
using the following link: https://biit.cs.ut.ee/
gplink/l/3i6bF7IGRS.





Identify enriched transcription factors of differentially expressed genes
=================
