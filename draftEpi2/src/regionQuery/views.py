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
        region_list[i] = region_list[i].split(':')
        region_list[i] = [region_list[i][0].strip(), region_list[i][1].split('-')[0].strip(), region_list[i][1].split('-')[1].strip()]
        # now we have a list where every entry has three values, the chromosome, the start and the end
    return region_list


def region_search_view(request):

    error_msg = ''

    query = request.POST.get('geneRegions')
    cell_types = request.POST.get('cellTypes')[:-2]  # directly getting rid of the last comma and whitespace
    csv_file = request.POST.get('csvFile')
    print(csv_file)
    activ_thresh = request.POST.get('activ_thresh')
    if len(activ_thresh) > 0:
        try:
            activ_thresh = float(activ_thresh)
        except ValueError:
            activ_thresh = 0.0
    else:
        activ_thresh = 0.0

    if len(query) == 0:
        csv_list = [x.strip() for x in csv_file.split(',') if x != '' and x != ' ']
        csv_list = [x for x in csv_list if x != '']  # because of possible empty lines
        print(csv_list)
        region_counter = 0
        for i in range(int(len(csv_list)/3)):
            if 'chr' not in csv_list[region_counter*3].lower():
                csv_list[region_counter*3] = 'chr' + str(csv_list[region_counter*3])
            this_region = str(csv_list[region_counter*3]).lower() + ":" + str(csv_list[region_counter*3+1]) + '-' + str(csv_list[region_counter*3+2]) + ", "
            query = query + this_region
            region_counter += 1
    if len(query) == 0:
        query = request.POST.get('chrField') + ":" + str(request.POST.get('chrStart')) + "-" + str(request.POST.get('chrEnd')) + ",'"
    print(query)

    if len(cell_types) > 0:
        cell_types_list = cell_types.split(', ')
    else:
        cell_types_list = []

    cell_types_list_upper = [x.capitalize() for x in cell_types_list]

    query_list = clear_chr_string(query)

    try:
        query_list = list(set(query_list))  # with use of set, we update our query
    # list, so we only have unique values in it
    except TypeError:  # continue if set throws an error
        pass

    query_list_string = query[:-2]
    # get our export string. We shorten it if it has too many entries
    comma_pos = [pos for pos, char in enumerate(query_list_string) if char == ',']
    if len(comma_pos) > 2:
        export_string = query_list_string[:comma_pos[2]] + '...' + str(len(comma_pos)-2) + ' more'
    else:
        export_string = query_list_string

    data = API_Region(query_list, cell_types_list, activ_thresh)

    template = 'regionQuery_search.html'
    if len(data) == 0:
        template = 'empty_data.html'  # we switch the template if there is no data
        if activ_thresh != 0.0:
            error_msg = 'No REMs were found that match your query settings. You might want to try lowering the ' \
                        'activity threshold or modifying the region boundaries.'
        if activ_thresh == 0.0:
            error_msg = 'No REMs were found in your selected regions. You might want to try ' \
                        'changing the region boundaries.'


    context = {
        'data': data,
        'error_msg': error_msg,
        'query_string': query_list_string,
        'export_string': export_string,
        'cell_types_string': cell_types,
        'cell_types_list': cell_types_list,
        'cell_types_list_upper': cell_types_list_upper,
        'activ_thresh': activ_thresh,
    }
    return render(request, template, context)


