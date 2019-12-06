from django import template

register = template.Library()

@register.simple_tag
def get_cellType_attr(obj, cellType, is_activity_or_samplecount):
    if is_activity_or_samplecount == 'activity':
        attr = round(obj[cellType+'_dnase1Log2'], 5)
    if is_activity_or_samplecount == 'samplecount':
        attr = obj[cellType+'_samplecount']
    return attr
