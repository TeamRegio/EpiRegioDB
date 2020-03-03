from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from table_manager.models import genomeAnnotation, geneExpression, sampleInfo, cellTypes, REMActivity, REMAnnotation, geneAnnotation
from geneQuery.views import search_cellTypes
from API import API_Region
# Works similar to the geneID Query app. The views file there is commented more detailed

def regionQuery_view(request):
    return render(request, 'regionQuery.html')


def clear_chr_string(query):
    region_list = query.split(';')[:-1]  # the last entry is just the empty string after the comma
    for i in range(len(region_list)):
        region_list[i] = region_list[i].split(':')
        region_list[i] = [region_list[i][0].strip(), region_list[i][1].split('-')[0].strip(), region_list[i][1].split('-')[1].strip()]
        # now we have a list where every entry has three values, the chromosome, the start and the end
    return region_list


def region_search_view(request):

    error_msg = ''

    query = request.POST.get('geneRegions')
    cell_types = request.POST.get('cellTypes')[:-2]  # directly getting rid of the last comma and whitespace
    activ_thresh = request.POST.get('activ_thresh')
    overlap = request.POST.get('overlap')

    csv_file = request.POST.get('csvFile')
    csv_file_name = request.POST.get('csv_upload')
    csv_file_rows = request.POST.get("csvFileRows")
    # print(csv_file)
    if len(activ_thresh) > 0:
        try:
            activ_thresh = float(activ_thresh)
        except ValueError or TypeError:
            activ_thresh = 0.0
    else:
        activ_thresh = 0.0

    if len(overlap) > 0:
        try:
            overlap = float(overlap)
        except ValueError or TypeError:
            overlap = 100
    else:
        overlap = 100

    if len(csv_file) > 0:
        query = ''  # if we have a csv-file we discard any selected regions

        if csv_file_name[-3:].lower() == 'csv' or csv_file_name[-3:].lower() == 'txt':  # we treat csv files different than bed files
            csv_list = [x.strip() for x in csv_file.split(',') if x != '' and x != ' ']
            csv_list = [x for x in csv_list if x != '']  # because of possible empty lines

        elif csv_file_name[-3:].lower() == 'bed':

            comma_counter = 0  # get the number of blank lines at the end, indicated by commas
            for n in range(1, len(csv_file)):
                if csv_file[n*-1] == ',':
                    comma_counter += 1
                else:
                    break  # stop the for loop when we found sth else than comma
            csv_file_rows = int(csv_file_rows) - comma_counter  # subtract to get the number of filled rows

            csv_list = [x.strip() for x in csv_file.split(',') if x != '' and x != ' ' and x != ',']
            csv_list_cleaned = []
            for row in range(csv_file_rows):
                row_start = int(row*(len(csv_list)/csv_file_rows))
                csv_list_cleaned += csv_list[row_start:row_start+3]  # we only take the
            # first three values, as in bed files all the other columns are irrelevant for us
            csv_list = csv_list_cleaned

        else:  # not really possible up to this point, but just to be sure
            csv_list = []

        region_counter = 0
        for i in range(int(len(csv_list)/3)):  # it's a repeated step to first convert it into a formatted string just
            # to convert it back into a list with the clear_csv function again. But we need the export strings and
            # have a more uniform transformation this way
            if 'chr' not in csv_list[region_counter*3].lower():
                csv_list[region_counter*3] = 'chr' + str(csv_list[region_counter*3])
            this_region = str(csv_list[region_counter*3]).lower() + ":" + str(csv_list[region_counter*3+1]) + '-' + str(csv_list[region_counter*3+2]) + ", "
            query = query + this_region
            region_counter += 1

    if len(query) == 0:
        query = request.POST.get('chrField') + ":" + str(request.POST.get('chrStart')) + "-" + str(request.POST.get('chrEnd')) + ",'"

    if len(cell_types) > 0:
        cell_types_list = cell_types.split('; ')
    else:
        cell_types_list = []

    cell_types_list_upper = [x.capitalize() for x in cell_types_list]

    query_list = clear_chr_string(query.replace(",", ";"))

    try:
        query_list = list(set(query_list))  # with use of set, we update our query
    # list, so we only have unique values in it
    except TypeError:  # continue if set throws an error
        pass

    query_list_string = query[:-2]
    # get our export string. We shorten it if it has too many entries
    comma_pos = [pos for pos, char in enumerate(query_list_string) if char == ',']
    if len(comma_pos) > 2:
        export_string = query_list_string[:comma_pos[2]].replace(" ", "") + '...' + str(len(comma_pos)-2) + 'more'
        query_list_string = query_list_string[:comma_pos[2]] + ' and ' + str(len(comma_pos)-2) + ' more'
    else:
        export_string = query_list_string.replace(" ", '')

    data, no_hit, invalid_list = API_Region(query_list, cell_types_list, overlap, activ_thresh)

    no_data = []  # for the regions we need to format it into a list of strings, to be consequent with the
    # chrX:start-end format
    if len(no_hit) >= 1:
        for i in range(len(no_hit)-1):
            no_data.append(no_hit[i][0]+':'+str(no_hit[i][1])+'-'+str(no_hit[i][2])+', ')
        no_data.append(no_hit[-1][0]+':'+str(no_hit[-1][1])+'-'+str(no_hit[-1][2]))

    invalid_string_list = []
    if len(invalid_list) >= 1:
        for i in range(len(invalid_list)-1):
            invalid_string_list.append(invalid_list[i][0]+':'+str(invalid_list[i][1])+'-'+str(invalid_list[i][2]) + ", ")
        invalid_string_list.append(invalid_list[-1][0]+':'+str(invalid_list[-1][1])+'-'+str(invalid_list[-1][2]))

    template = 'regionQuery_search.html'
    if len(data) == 0:
        template = 'empty_data.html'  # we switch the template if there is no data
        if activ_thresh != 0.0 and overlap == 100:
            error_msg = 'No REMs were found that match your query settings. You might want to try lowering the ' \
                        'activity threshold, change the overlap or modifying the region boundaries.'
        if activ_thresh == 0.0 and overlap == 100:
            error_msg = 'No REMs were found in your selected regions. You might want to try ' \
                        'changing the overlap or modifying the region boundaries.'

    context = {
        'data': data,
        'error_msg': error_msg,
        'query_string': query_list_string,
        'export_string': export_string.replace(':', "-"),
        'cell_types_string': cell_types,
        'cell_types_list': cell_types_list,
        'cell_types_list_upper': cell_types_list_upper,
        'activ_thresh': activ_thresh,
        'no_data': no_data,
        'invalid_list': invalid_string_list,
        "overlap": int(overlap),
    }

    return render(request, template, context)

