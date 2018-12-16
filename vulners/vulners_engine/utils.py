from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from .forms import FilterForm
from .models import Vulner

import requests
import json


def get_vulners_info(vendor=None, vulner=None, skip=None):
    params = {
        'query': 'type:{}'.format(vendor),
        'id': '"{}"'.format(vulner),
        'skip': skip
    }
    vulners = requests.get(
        'https://vulners.com/api/v3/search/lucene/', params=params)
    print(vulners.url)
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
        print('FILTERS ARE: {}'.format(filters))
        vendor = filters['vendor']
        vulner = filters['vulner']
    return [vendor, vulner, skip]
