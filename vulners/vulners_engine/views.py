from django.shortcuts import render
from django.views import generic

from .models import Vulner
from .forms import FilterForm
from .utils import get_vulners_info
from .utils import get_skip_to_paginate
from .utils import get_form_request_params

from datetime import datetime


class VulnersListView(generic.ListView):
    def get(self, request):
        form = FilterForm(request.GET or None)
        vendor, vulner, skip = get_form_request_params(form, request)
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
                            'published': datetime.strptime(vulner['_source']['published'], '%Y-%m-%dT%H:%M:%S')
                        })
        return render(request, 'vulners_list.html', context={
                                    'form': form,
                                    'vulners_list': vulners_list,
                                    'skip': skip})
