from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from table_manager.models import *
from geneQuery.views import search_cellTypes, strip_csv_query, crem_view
from API import *


def remQuery_view(request):
    return render(request, 'remQuery.html')


# def search_for_rems(query_list):  # We look up in our REMAnnotation table, which objects fit the entered GeneIDs and
#     # return them in a list
#     hit_list = []
#     for i in query_list:
#         data_set = REMAnnotation.objects.filter(REMID=i)
#         for single_obj in data_set:
#             single_obj.pValue = round(10**(float(single_obj.pValue)), 6)  # provisional way to round
#             single_obj.regressionCoefficient = round(float(single_obj.regressionCoefficient), 6)
#             hit_list.append(single_obj)
#     return hit_list  # our list of objects, fitting the query_list


def rem_search_view(request):

    query = request.POST.get('REMIDs').upper()
    query = query.replace(',', ';')
    csv_file = request.POST.get('csvFile').upper()

    score_thresh_input = request.POST.get('score_thresh')
    activ_thresh = request.POST.get('activ_thresh')
    if len(activ_thresh) > 0:  # everything we get back via POST.get is a string, so we don't have to check if len works
        try:
            activ_thresh = float(activ_thresh)
        except ValueError:
            activ_thresh = 0.0
    else:
        activ_thresh = 0.0

    if len(score_thresh_input) > 0:  # everything we get back via POST.get is a string, so we don't have to check if len works
        try:
            if '|' in score_thresh_input:
                score_thresh = ['abs']
            else:
                score_thresh = ['no']
            score_thresh_input = score_thresh_input.replace("|", "").split(',')
            score_thresh += [float(x.replace(' ', '')) for x in score_thresh_input]
        except ValueError or AttributeError:
            score_thresh = ['no', -1, 1]
    else:
        score_thresh = ['no', -1, 1]

    cell_types = request.POST.get('cellTypes')[:-2]  # directly getting rid of the last comma and whitespace
    if len(cell_types) > 0:
        cell_types_list = cell_types.split('; ')
    else:
        cell_types_list = []

    cell_types_list_upper = [x.capitalize() for x in cell_types_list]

    # If a file is there, we take it and forget the rest
    if len(csv_file) > 0:
        query = csv_file.replace(',', ";")

    query_list = strip_csv_query(query)[0]
    query_list_string = strip_csv_query(query)[1]
    if len(query_list) > 3:  # if the number of queried genes is too high, we take only three to shorten the export name
        export_string = strip_csv_query(query)[2].replace(" ", '') + '...' + str(len(query_list)-3) + 'more'
        query_list_string = strip_csv_query(query)[2].replace("_", ", ") + ' and ' + str(len(query_list)-3) + ' more'
    else:
        export_string = query_list_string.replace(" ", '')

    data, invalid_list = API_REMID(query_list, cell_types_list, score_thresh, activ_thresh)
    template = 'remQuery_search.html'
    error_msg = ''

    for i in range(len(invalid_list)-1):
        invalid_list[i] += ', '

    if len(data) == 0:
        template = 'empty_data.html'  # we switch the template if there is no data
        if activ_thresh == 0 and score_thresh == ['no', -1, 1]:
            error_msg = 'No REMs were found that match your query settings.'
        if activ_thresh != 0 or score_thresh != ['no', -1, 1]:
            error_msg = 'No REMs were found that match your query settings. You might want to try lowering the ' \
                    'activity threshold.'

    gP_link, num_genes = gProfiler_link(data)  # use the API function to get the correct link

    context = {
        'data': data,
        'query_string': query_list_string,
        'export_string': export_string,
        'cell_types_string': cell_types,
        'cell_types_list': cell_types_list,
        'cell_types_list_upper': cell_types_list_upper,
        'activ_thresh': activ_thresh,
        'score_thresh': score_thresh,
        'error_msg': error_msg,
        'invalid_list': invalid_list,
        'version': 1,
        'gP_link': gP_link,
        'num_genes': num_genes
    }
    return render(request, template, context)
