from django.shortcuts import render
from .forms import FilterForm
from django.views import generic
from .models import Vulner
from django.core.exceptions import ObjectDoesNotExist

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


class VulnersListView(generic.ListView):

    def get(self, request):
        form = FilterForm(request.GET or None)
        increment = 20
        vendor = None
        vulner = None
        print('REQUEST POST {}'.format(request.POST))
        if request.GET.get('skip', 0):
            skip = int(request.GET.get('skip', 0))
            skip += increment
            print('HERE_1')
        else:
            skip = int(request.GET.get('skip_prev', 0))
            skip -= increment
            if skip <= 0:
                skip = 0
            print('HERE_2')
        print(form)
        print('{} {} {}'.format(vendor, vulner, skip))
        if form.is_valid():
            filters = form.cleaned_data
            print('FILTERS ARE: {}'.format(filters))
            vendor = filters['vendor']
            vulner = filters['vulner']
        vulners = get_vulners_info(vendor, vulner, skip)
        vln_lst = []
        if vulners:
            for i in vulners['data']['search']:
                vln_lst.append(i['_source'])
        return render(request, 'vulners_list.html', context={
                                    'form': form,
                                    'vulners_list': vln_lst,
                                    'skip': skip})




    def post(self, request):
        form = FilterForm(request.POST or None)
        increment = 20
        vendor = None
        vulner = None
        print('REQUEST POST {}'.format(request.POST))
        if request.GET.get('skip', 0):
            skip = int(request.GET.get('skip', 0))
            skip += increment
            print('HERE_1')
        else:
            skip = int(request.GET.get('skip_prev', 0))
            skip -= increment
            if skip <= 0:
                skip = 0
            print('HERE_2')
        print(form)
        print('{} {} {}'.format(vendor, vulner, skip))
        if form.is_valid():
            filters = form.cleaned_data
            print('FILTERS ARE: {}'.format(filters))
            vendor = filters['vendor']
            vulner = filters['vulner']
        vulners = get_vulners_info(vendor, vulner, skip)
        vln_lst = []
        if vulners:
            for i in vulners['data']['search']:
                vln_lst.append(i['_source'])
                try:
                    obj = Vulner.objects.get(vulner=i['_source']['id'])
                    print(obj)
                except Vulner.DoesNotExist:
                    obj = Vulner(
                        vulner=i['_source']['id'],
                        vendor=i['_source']['type'],
                        description=i['_source']['description'],
                        published=i['_source']['published'])
                    obj.save()

        return render(request, 'vulners_list.html', context={
                                    'form': form,
                                    'vulners_list': vln_lst,
                                    'skip': skip})
