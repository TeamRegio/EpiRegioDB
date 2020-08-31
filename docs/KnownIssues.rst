Known Issues
============

Here we discuss some of the known issues, and what you can do to rectify it. All issues we discuss here are what we have learned from our testing on the browsers/OS listed below.

+-------------+--------+------+---------+-------+
|OS/Browser   | Chrome | Edge |	Firefox | Safari|
+=============+========+======+=========+=======+
|Linux        |    x   |      |    x    |       |
+-------------+--------+------+---------+-------+
|MacOS        |    x   |      |    x    |       |
+-------------+--------+------+---------+-------+
|Windows      |    x   |   x  |    x    |       |
+-------------+--------+------+---------+-------+


Layout issues
------------------
If you find elements on the website overlapping with each other, you could try clearing the cache of your browser or try it in private mode. If it still overlaps, try updating to a newer version of your browser. We developed our website in the newest browser version in private mode.


Server Error (500)
------------------

Issue: One of the parameters you have set is wrong! 

Solution: If you are using Chrome, please try to clear the cache in your browser, and try again. Still the issue persists? Please check all your inputs, and the options you selected.

We are aware of issues causing a Server Error 500 if the input list is too large. We are working on solving this issue. In the meantime, unfortunately, you might have to try to provide your input in smaller chunks.

The issue with the gene name – ensembl id mapping
------------------
In general, we advise to use the ensembl ids of the genes of interest instead of the gene name, since EpiRegio does not store all gene name aliases. 
If you are interested in the gene Y_RNA, please stick to the ensembl id to avoid any confusions. EpiRegio stores REMs for roughly 300 genes with the gene name Y_RNA (according the gencode.v26.annotation.gtf file). However, all of them have a different ensembl id to identify them uniquely.  

If you face other problems, please let us know through `GitHub issues <https://github.com/TeamRegio/EpiRegioDB/issues>`_!

