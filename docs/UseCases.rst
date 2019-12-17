Query Guide
---------
Here we provide a step-by-step guide for every query available, including an explanation of the output. Every query has an "Examplary Query" button at the  bottom of the page. Try it out to see how a valid query would look like. 

Gene Query
=================

Do you wish to search for Regulatory Elements (REMs) related to a specific gene? 

a. Go to the *Gene Query* tab. 
b. You can choose to search either with Ensembl IDs or gene symbols. The version number of Ensembl IDs is not required. When entering gene symbols, you can add suggestions on the right by clicking on the appearing buttons. Selected buttons will be listed underneath 'Currently selected:'. Deselect your choices by reclicking on those buttons. We use the human genome hg38.

.. image:: ./images/geneQuery_form.png

c. When you have multiple IDs or symbols to search, separate them by comma in the input field or make a CSV file and upload it. A combination of the input field and uploaded file is not implemented.

d. Choosing cell types/tissues:

.. image:: ./images/geneQuery_cellTypes.png
Start typing in the cell type/tissue of your interest, and the server suggests the available cell types matching your query. You can only choose from them. To select a cell type/tissue click on the button on the right. To deselect click again on the button below 'Currently selected:'. The DNase activity of the REMs associated with your chosen genes will be added as columns to the output table for all the cell types/tissues you selected.
Once you selected a cell type/tissue, a new input field will appear, which gives the option to choose an activity threshold. This threshold refers to the DNase activity of the REMs in the cell types/tissues. Only REMs that exceed the threshold in ALL of the cell types/tissues you selected will be shown in the output table. Leave the field empty to get back all REMs independent of their activity. 

e. The result page shows the information based on your query settings. All the REMs that are associated to your queried genes are listed with their location, their predicted function, the model score, the REM cluster they are belonging to and their activity in the cell types/tissues you selected. The *model score* indicates how important a REM is for its associated gene over all cell types/tissues. The higher the value, the more important the REM is. The next column *Associated REM cluster* contains the ID of the cluster this REM is contained in. A cluster of REMs consists of all the REMs that overlap by at least 1 bp. Click on CREM ID to get more information. If you selected cell types/tissues in your query, the DNase *activity* of the REMs in these cell types/tissues will be shown as mean over all the samples n in our database.
You can export the able as xls-, csv- or pdf-file. For more details on the genes you queried, click on the link at the top of the table.

.. image:: ./images/geneQuery_table.png


Region based search
===================

Do you wish to search for Regulatory Elements (REMs) being located in a specific genomic region? 

a. Go to the *Region Query* tab. 
b. You can enter a region by choosing a chromosome, the start and the end point and then clicking on the *select* button. Add as many regions as you like. Deselect your choices by reclicking on the added buttons. 

.. image:: ./images/regionQuery_form.png

c. You can also upload a CSV file with your regions of interest in which the first value has to be the chromosome, followed by the start and the end positio and upload it. A combination of input field and uploaded file is not implemented.

d. Choosing cell types/tissues:

.. image:: ./images/geneQuery_cellTypes.png
Start typing in the cell type/tissue of your interest, and the server suggests the available cell types matching your query. You can only choose from them. To select a cell type/tissue click on the button on the right. To deselect click again on the button below 'Currently selected:'. The DNase activity of the REMs associated with your chosen genes will be added as columns to the output table for all the cell types/tissues you selected.
Once you selected a cell type/tissue, a new input field will appear, which gives the option to choose an activity threshold. This threshold refers to the DNase activity of the REMs in the cell types/tissues. Only REMs that exceed the threshold in ALL of the cell types/tissues you selected will be shown in the output table. Leave the field empty to get back all REMs independent of their activity. 

e. The result page shows the information based on your query settings. All the REMs that are associated to your queried genes are listed with their location, their predicted function, the model score, the REM cluster they are belonging to and their activity in the cell types/tissues you selected. The *model score* indicates how important a REM is for its associated gene over all cell types/tissues. The higher the value, the more important the REM is. The next column *Associated REM cluster* contains the ID of the cluster this REM is contained in. A cluster of REMs consists of all the REMs that overlap by at least 1 bp. Click on CREM ID to get more information. If you selected cell types/tissues in your query, the DNase *activity* of the REMs in these cell types/tissues will be shown as mean over all the samples n in our database.
You can export the able as xls-, csv- or pdf-file. For more details on the genes you queried, click on the link at the top of the table.

.. image:: ./images/geneQuery_table.png



xxREM based search
=================

xx
