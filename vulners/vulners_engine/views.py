from django.shortcuts import render
from .forms import FilterForm
from django.views import generic

import requests
import json


def get_vulners_info(vendor, vulner, skip):
    params = {
        'query': 'type:{}'.format(vendor),
        #'id': vulner,
        'skip': int(skip)

    }
    vulners = requests.get(
        'https://vulners.com/api/v3/search/lucene/', params=params).json()

    return  vulners #json.loads(vulners)


class VulnersListView(generic.ListView):
    # template_name = 'vulners_engine/vulners_list.html'


    def get(self, request):
        form = FilterForm(request.GET or None)
        increment = 20
        vendor = None
        vulner = None
        # if not vendor:
        #     return render(request, 'vulners_list.html', context={'form': form})
        # try:
        if request.GET.get('skip', 0):
            skip = int(request.GET.get('skip', 0))
            skip += increment
            # else:
            #     skip = int(request.GET.get('skip', 20))
            #     skip += increment
                # int(request.GET['skip_prev'])
                # skip -= increment
        else: # KeyError:
            # print(request.GET, 'HERERERE')
            skip = int(request.GET.get('skip_prev', 0))
                # skip = 0
            # else:
                # skip = int(request.GET.get('skip_prev', 0))
            skip -= increment
            if skip <= 0:
                skip = 0
        # except MultiValueDictKeyError:
        #     skip = 0
        print(form)
        print('{} {} {}'.format(vendor, vulner, skip))
        #     print('SKIP FIRST {}'.format(request.GET['skip'][0]))
        if form.is_valid():
            filters = form.cleaned_data
            print('FILTERS ARE: {}'.format(filters))
            vendor = filters['vendor']
            vulner = filters['vulner']
        vulners = get_vulners_info(vendor, vulner, skip)
        # print(vulners['data']['search'][0]['_source']['id'])
        vln_lst = []
        if vulners:
            for i in vulners['data']['search']:
                vln_lst.append(i['_source'])
        print(request.GET)
        print('SKIP {}'.format(skip))
        return render(request, 'vulners_list.html', context={'form': form,
                        'vulners_list': vln_lst,
                        'skip': skip})

    # def post(self, request):
    #     bound_form = PostForm(request.POST)
    #     if bound_form.is_valid():
    #         new_post = bound_form.save()
    #         return redirect(new_post)
    #     return render(request, 'blog/post_create.html', context={'form':bound_form})
