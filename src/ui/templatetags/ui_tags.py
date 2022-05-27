from django import template
import os

register = template.Library()


# thanks to https://stackoverflow.com/a/16649471

from urllib.parse import urlencode
from collections import OrderedDict

@register.simple_tag
def url_replace(request, field, value, direction=''):
    dict_ = request.GET.copy()

    if field == 'order_by' and field in dict_.keys():          
      if dict_[field].startswith('-') and dict_[field].lstrip('-') == value:
        dict_[field] = value
      elif dict_[field].lstrip('-') == value:
        dict_[field] = "-" + value
      else:
        dict_[field] = direction + value
    else:
      dict_[field] = direction + value

    return urlencode(OrderedDict(sorted(dict_.items())))

@register.filter
def env(key):
    return os.environ.get(key, None)