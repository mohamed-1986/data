import json
from django import template

from instapp.models import Manual, manual_category

register = template.Library()

@register.inclusion_tag('PID_unit_tag.html')
def unit_list():
    with open('units.json') as f:
        data = json.load(f)
    return {'data' : data['units']}



@register.inclusion_tag('temptag_manual.html')
def manual_cat_list():
    q_keys = []
    q_values = []
    for x,y in manual_category:
        q_keys.append(y)
        q_values.append(x)
    return { 'data' : q_keys }