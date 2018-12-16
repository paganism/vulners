from django.shortcuts import render
from .forms import FilterForm
from django.views import generic
from .models import Vulner
from django.core.exceptions import ObjectDoesNotExist

from .utils import get_vulners_info
from .utils import get_skip_to_paginate
from .utils import get_form_request_params


class VulnersListView(generic.ListView):
    def get(self, request):
        form = FilterForm(request.GET or None)
        vendor = None
        vulner = None
        skip = get_skip_to_paginate(request)
        if form.is_valid():
            filters = form.cleaned_data
            print('FILTERS ARE: {}'.format(filters))
            vendor = filters['vendor']
            vulner = filters['vulner']
        vulners = get_vulners_info(vendor, vulner, skip)
        if vulners:
            vulners_list = [vulner['_source'] for vulner in vulners['data']['search']]
        return render(request, 'vulners_list.html', context={
                                    'form': form,
                                    'vulners_list': vulners_list,
                                    'skip': skip})

    def post(self, request):
        form = FilterForm(request.GET or None)
        vendor, vulner, skip = get_form_request_params(form, request)
        print('VENDOR {}, VULNER {}, SKIP {}'.format(vendor, vulner, skip))
        vulners = get_vulners_info(vendor, vulner, skip)
        vulners_list = []
        if vulners:
            for vulner in vulners['data']['search']:
                vulners_list.append(vulner['_source'])
                obj, created = Vulner.objects.get_or_create(vulner=vulner['_source']['id'],
                    defaults={
                            'vulner': vulner['_source']['id'],
                            'vendor': vulner['_source']['type'],
                            'description': vulner['_source']['description'],
                            'published': vulner['_source']['published']
                        })
        return render(request, 'vulners_list.html', context={
                                    'form': form,
                                    'vulners_list': vulners_list,
                                    'skip': skip})
