from django import template

register = template.Library()

@register.simple_tag
def get_cellType_attr(obj, cellType, is_activity_or_samplecount):
    cellType = cellType.lower()
    if is_activity_or_samplecount == 'activity':
        attr = round(obj[cellType+'_dnase1Log2'], 7)
    elif is_activity_or_samplecount == 'samplecount':
        attr = obj[cellType+'_samplecount']
    elif is_activity_or_samplecount == 'score':
        attr = round(obj[cellType+'_score'], 7)
    else:
        attr = ""
    return attr
