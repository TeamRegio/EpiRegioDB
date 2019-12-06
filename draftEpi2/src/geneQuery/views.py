from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from table_manager.models import *
from API import API_SymbolToENSG, API_ENSGID, API_ENSGID_geneInfo, API_CREM_overview


# The first view only renders our HTML form where we can set our filters.
# After entering the filter settings, we get redirected to the geneQuery_search URL. On the way there
# our filter settings are collected, and the respective information is displayed.

# Our view function here is really short, as we do not import any django forms but write them all in the HTML file.
def geneQuery_view(request):
    return render(request, 'geneQuery.html')


# To be able to return the Query as string (to display and to name the export-files), we clean
# it up:
def strip_csv_query(query):
    query = [x.split()[0] for x in query.split(',') if x != '' and x != ' ']  # We write a list out of the csv input string
    query_cleaned_string = ""
    export_string = ""
    for i in query:
        query_cleaned_string = query_cleaned_string+', '+str(i)  # The cleanup is there to remove any empty entries
        # or unnecessary commas
    if len(query) > 3:
        for i in range(3):
            export_string = export_string + ', ' + str(query[i])
    return query, query_cleaned_string[1:], export_string[1:]  # from 1, because 0 is a comma


# def search_for_geneID(query_list):  # We look up in our REMAnnotation table, which objects fit the entered GeneIDs and
#     # return them in a list
#     hit_list = []
#     for i in query_list:
#         data_set = REMAnnotation.objects.filter(geneID=i)
#         for single_obj in data_set:
#             single_obj.pValue = round(10**(float(single_obj.pValue)), 6)  # provisional way to round
#             single_obj.regressionCoefficient = round(float(single_obj.regressionCoefficient), 6)
#             hit_list.append(single_obj)
#     return hit_list  # our list of objects, fitting the query_list


def gene_search_view(request):  # We grab all the submitted inputs, store them in the context and pass it on to our
    # geneQuery_search html

    gene_format = request.POST.get('gene_format')
    csv_file = request.POST.get('csvFile')

    activ_thresh = request.POST.get('activ_thresh')
    if len(activ_thresh) > 0:
        activ_thresh = float(activ_thresh)
    else:
        activ_thresh = 0

    if gene_format == 'id_format':
        query = request.POST.get('geneID_numeric')  # if it's numeric, we just want to get the string in the field

    else:
        query = request.POST.get('geneSymbol')  # our hidden html that stores the content of the selected buttons
        if len(query) == 0:  # if someone doesn't use the buttons, we look at the input field
            query = request.POST.get('geneID_symbolic')  # this is our input field with the string
    # If a file is there, we take it and forget the rest
    if len(csv_file) > 0:
        query = csv_file

    cell_types = request.POST.get('cellTypes')[:-2]  # the hidden html element storing the content of the selected cell
    # types buttons and we directly get rid of the last comma and whitespace
    if len(cell_types) > 0:
        cell_types_list = cell_types.split(', ')
    else:
        cell_types_list = []

    query_list = strip_csv_query(query)[0]
    query_list_string = strip_csv_query(query)[1]

    if len(query_list) > 3:  # if the number of queried genes is too high, we take only three to shorten the export name
        export_string = strip_csv_query(query)[2] + '...' + str(len(query_list)-3) + ' more'
    else:
        export_string = query_list_string

    if gene_format == 'symbol_format':  # in case of geneSymbol as query we first have to look up the respective
        # ensemble ID
        query_list = API_SymbolToENSG(query_list)  # our API function to convert geneSymbols to ENSG IDs

    data = API_ENSGID(query_list, cell_types_list, activ_thresh)
    if len(data) == 0:
        data = None  # if so, we don't display any table in the view

    context = {
        'data': data,
        'query_string': query_list_string,
        'export_string': export_string,
        'cell_types_list': cell_types_list,
    }
    return render(request, 'geneQuery_search.html', context)


def search_geneSymbol(request):  # the function is called by ajax via the url set in the ajax file
    if request.method == "POST":
        search_text_gene = request.POST['search_text_gene']  # grab the string in the input field
    else:
        search_text_gene = ''
    if 3 <= len(search_text_gene):  # only start looking when there's three chars entered
        geneSymbol_search = geneAnnotation.objects.filter(geneSymbol__contains=search_text_gene.upper()).values('geneSymbol')[:30]  # collect a maximum of 30 hits
    else:
        geneSymbol_search = ''
    return render_to_response('ajax_search_genesymbol.html',
                              {'geneSymbol_search': geneSymbol_search, 'search_text_len': len(search_text_gene)})


def search_cellTypes(request):
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''
    if 1 <= len(search_text):
        matching_samples = sampleInfo.objects.filter(cellTypeID__cellTypeName__contains=search_text.lower()).values_list('cellTypeID', 'cellTypeID__cellTypeName', flat=False)
        cellType_search = []
        for i in matching_samples:  # get rid of double entries
            if i not in cellType_search:
                cellType_search.append(i)
        print(cellType_search)
    else:
        cellType_search = ''

    return render_to_response('ajax_search_celltypes.html',
                              {'cellType_search': cellType_search[:15], 'search_text_len': len(search_text), 'len_hits': len(cellType_search)})


# CREM VIEWS ####################################################################

def search_for_rems(query_list):  # For the placeholder data we look for REMs
    hit_list = []
    data_set = REMAnnotation.objects.filter(REMID=query_list)
    print(data_set)
    for single_obj in data_set:
        single_obj.pValue = round(10**(float(single_obj.pValue)), 6)  # provisional way to round
        single_obj.regressionCoefficient = round(float(single_obj.regressionCoefficient), 6)
        hit_list.append(single_obj)
    return hit_list  # our list of objects, fitting the query_list


def crem_view(request, CREMID):

    context = {
        'data': API_CREM_overview(CREMID),
        'query': CREMID,
    }
    return render(request, 'linked_crem.html', context)


# GENE DETAILS VIEW ####################################################################

def gene_details_view(request):
    queried_genes = request.POST.get('query_string')
    print("genedetailsview")
    print(queried_genes)
    context = {
        'gene_info': API_ENSGID_geneInfo(queried_genes),
    }
    return render(request, 'gene_details.html', context)

