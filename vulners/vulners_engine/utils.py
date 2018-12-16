import requests


def get_vulners_info(vendor=None, vulner=None, skip=None):
    params = {
        'query': 'type:{}'.format(vendor),
        'id': '"{}"'.format(vulner),
        'skip': skip
    }
    vulners = requests.get(
        'https://vulners.com/api/v3/search/lucene/', params=params)
    return vulners.json()


def get_skip_to_paginate(request):
    increment = 20
    if request.GET.get('skip', 0):
        skip = int(request.GET.get('skip', 0))
        skip += increment
    else:
        skip = int(request.GET.get('skip_prev', 0))
        skip -= increment
        if skip <= 0:
            skip = 0
    return skip


def get_form_request_params(form, request):
    vendor = None
    vulner = None
    skip = get_skip_to_paginate(request)
    if form.is_valid():
        filters = form.cleaned_data
        vendor = filters['vendor']
        vulner = filters['vulner']
    return [vendor, vulner, skip]
