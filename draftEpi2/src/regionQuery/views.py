from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from table_manager.models import genomeAnnotation, geneExpression, sampleInfo, cellTypes, REMActivity, REMAnnotation, geneAnnotation
from geneQuery.views import search_cellTypes
from API import API_Region
# Works similar to the geneID Query app. The views file there is commented more detailed

def regionQuery_view(request):
    return render(request, 'regionQuery.html')


def clear_chr_string(query):
    region_list = query.split(',')[:-1]  # the last entry ist just the empty string after the comma
    for i in range(len(region_list)):
        region_list[i] = region_list[i].split()
        region_list[i] = [region_list[i][0], region_list[i][1].split('-')[0], region_list[i][1].split('-')[1]]
        # now we have a list where every entry has three values, the chromosome, the start and the end
    return region_list


def search_for_regions(query_list):  # We look up in our REMAnnotation table, which objects fit the entered GeneIDs and
    # return them in a list
    hit_list = []
    for i in query_list:
        data_set = REMAnnotation.objects.filter(chr=i[0], start__gte=i[1], end__lte=i[2])
        for single_obj in data_set:
            single_obj.pValue = round(10**(float(single_obj.pValue)), 6)  # provisional way to round
            single_obj.regressionCoefficient = round(float(single_obj.regressionCoefficient), 6)
            hit_list.append(single_obj)
    return hit_list  # our list of objects, fitting the query_list


def region_search_view(request):

    query = request.POST.get('geneRegions')
    cell_types = request.POST.get('cellTypes')[:-2]  # directly getting rid of the last comma and whitespace
    csv_file = request.POST.get('csvFile')

    activ_thresh = request.POST.get('activ_thresh')
    if len(activ_thresh) > 0:
        try:
            activ_thresh = float(activ_thresh)
        except ValueError:
            activ_thresh = 0
    else:
        activ_thresh = 0

    if len(query) == 0:
        csv_list = csv_file.split(',')
        region_counter = 0
        for i in range(int(len(csv_list)/3)):
            if 'chr' not in csv_list[region_counter*3]:
                csv_list[region_counter*3] = 'chr' + csv_list[region_counter*3]
            this_region = csv_list[region_counter*3] + " " + str(csv_list[region_counter*3+1]) + '-' + str(csv_list[region_counter*3+2]) + ", "
            query = query + this_region
            region_counter += 1
    if len(query) == 0:
        query = request.POST.get('chrField') + " " + str(request.POST.get('chrStart')) + "-" + str(request.POST.get('chrEnd')) + ",'"

    if len(cell_types) > 0:
        cell_types_list = cell_types.split(', ')
    else:
        cell_types_list = []

    query_list = clear_chr_string(query)
    query_list_string = query[:-2]
    # get our export string. We shorten it if it has too many entries
    comma_pos = [pos for pos, char in enumerate(query_list_string) if char == ',']
    if len(comma_pos) > 2:
        export_string = query_list_string[:comma_pos[2]] + '...' + str(len(comma_pos)-2) + ' more'
    else:
        export_string = query_list_string

    data = API_Region(query_list, cell_types_list, activ_thresh)
    if len(data) == 0:
        data = None  # if so, we don't display any table in the view

    cell_types_list_upper = [x.capitalize() for x in cell_types_list]

    context = {
        'data': data,
        'query_string': query_list_string,
        'export_string': export_string,
        'cell_types_list': cell_types_list,
        'cell_types_list_upper': cell_types_list_upper
    }
    return render(request, 'regionQuery_search.html', context)


