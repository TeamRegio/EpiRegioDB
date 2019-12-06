from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from table_manager.models import *
from geneQuery.views import search_cellTypes, strip_csv_query, crem_view
from API import API_REMID


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

    query = request.POST.get('REMIDs')
    csv_file = request.POST.get('csvFile')

    activ_thresh = request.POST.get('activ_thresh')
    if len(activ_thresh) > 0:
        activ_thresh = float(activ_thresh)
    else:
        activ_thresh = 0

    cell_types = request.POST.get('cellTypes')[:-2]  # directly getting rid of the last comma and whitespace
    if len(cell_types) > 0:
        cell_types_list = cell_types.split(', ')
    else:
        cell_types_list = []

    # If a file is there, we take it and forget the rest
    if len(csv_file) > 0:
        query = csv_file

    query_list = strip_csv_query(query)[0]
    query_list_string = strip_csv_query(query)[1]
    if len(query_list) > 3:  # if the number of queried genes is too high, we take only three to shorten the export name
        export_string = strip_csv_query(query)[2] + '...' + str(len(query_list)-3) + ' more'
    else:
        export_string = query_list_string

    data = API_REMID(query_list, cell_types_list, activ_thresh)
    if len(data) == 0:
        data = None  # if so, we don't display any table in the view

    context = {
        'data': data,
        'query_string': query_list_string,
        'export_string': export_string,
        'cell_types_list': cell_types_list,
    }
    return render(request, 'remQuery_search.html', context)
