from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from table_manager.models import *
from API import *


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
            export_string = export_string + '_' + str(query[i])
    return query, query_cleaned_string[1:], export_string[1:]  # from 1, because 0 is a comma


def gene_search_view(request):  # We grab all the submitted inputs, store them in the context and pass it on to our
    # geneQuery_search html

    error_msg = ''
    invalid_list = []

    gene_format = request.POST.get('gene_format')
    csv_file = request.POST.get('csvFile')

    activ_thresh = request.POST.get('activ_thresh')
    if len(activ_thresh) > 0:  # everything we get back via POST.get is a string, so we don't have to check if len works
        try:
            activ_thresh = float(activ_thresh)
        except ValueError:
            activ_thresh = 0.0
    else:
        activ_thresh = 0.0

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
    cell_types_list_upper = [x.capitalize() for x in cell_types_list]

    query_list = strip_csv_query(query)[0]
    query_list_string = strip_csv_query(query)[1]

    if len(query_list) > 3:  # if the number of queried genes is too high, we take only three to shorten the export name
        export_string = strip_csv_query(query)[2].replace(" ", '') + '...' + str(len(query_list)-3) + 'more'
    else:
        export_string = query_list_string.replace(" ", "")

    if gene_format == 'symbol_format':  # in case of geneSymbol as query we first have to look up the respective
        # ensemble ID
        query_list, invalid_list_symbol = API_SymbolToENSG(query_list)  # our API function to convert geneSymbols to ENSG IDs
        invalid_list = invalid_list_symbol  # if symbol format was chosen, we also want to give back the invalid list
        # as symbols

    data, no_data, invalid_list_ensembl = API_ENSGID(query_list, cell_types_list, activ_thresh, gene_format)  # data are
    # the hits, meaning the dictionaries, no_data are the genes for which there was no REM in the db

    if gene_format == 'id_format':
        invalid_list = invalid_list_ensembl

    template = 'geneQuery_search.html'
    if len(data) == 0:
        template = 'empty_data.html'  # we switch the template if there is no data
        if activ_thresh != 0.0:  # if we already have the geneSymbol error we want to keep it
            error_msg = 'No data was found that match your query settings. You might want to try modifying ' \
                        'the activity threshold.'
        if activ_thresh == 0.0:
            error_msg = 'The model did not find putative REMs that are associated with your queried genes.'

    context = {
        'data': data,
        'query_string': query_list_string,
        'export_string': export_string,
        'cell_types_string': cell_types,
        'cell_types_list': cell_types_list,
        'cell_types_list_upper': cell_types_list_upper,
        'activ_thresh': activ_thresh,
        'error_msg': error_msg,
        'no_data': no_data,
        'invalid_list': invalid_list,
    }
    # print(context)
    return render(request, template, context)


def search_geneSymbol(request):  # the function is called by ajax via the url set in the ajax file
    if request.method == "POST":
        search_text_gene = request.POST['search_text_gene']  # grab the string in the input field
    else:
        search_text_gene = ''
    if 2 <= len(search_text_gene):  # only start looking when there's three chars entered
        geneSymbol_search = API_geneSymbolValidation([search_text_gene])
    else:
        geneSymbol_search = ''
    return render_to_response('ajax_search_genesymbol.html',
                              {'geneSymbol_search': geneSymbol_search[:30], 'search_text_len': len(search_text_gene)})


def search_cellTypes(request):
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''
    if 1 <= len(search_text):
        cellType_search = API_cellTypesValidation([search_text])
    else:
        cellType_search = ''

    return render_to_response('ajax_search_celltypes.html',
                              {'cellType_search': cellType_search[:15], 'search_text_len': len(search_text), 'len_hits': len(cellType_search)})


def crem_view(request, CREMID):

    context = {
        'data': API_CREM_overview([CREMID]),
        'query': CREMID,
    }
    return render(request, 'linked_crem.html', context)


# GENE DETAILS VIEW ####################################################################

def gene_details_view(request, query_string):

    query_list = strip_csv_query(query_string)[0]
    query_list_list = query_list

    if query_list[0][:4] != 'ENSG':
        query_list, invalid_list = API_SymbolToENSG(query_list)

    if len(query_list) > 3:  # if the number of queried genes is too high, we take only three to shorten the export name
        export_string = strip_csv_query(query_string)[2] + '...' + str(len(query_list)-3) + ' more'
    else:
        export_string = query_string

    context = {
        'data': API_ENSGID_geneInfo(query_list),
        'query_list': query_list,
        'query_list_list': query_list_list,
        'query_string': query_string,
        'export_string': export_string,
    }
    # print(context)
    return render(request, 'gene_details.html', context)

