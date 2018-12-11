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
        # skip = 0
        # skip += increment
        #print('SKIP {}'.format(skip))
        try:
            skip = int(request.GET['skip_next'])
            if int(request.GET['skip_next']):
                skip += increment
            else:
                skip -= increment
            # print('HERE_1')
            # print('SKIP {}'.format(skip))
            # skip += increment
            # print('HERE_2')
            # print('SKIP {}'.format(skip))
            # print(type(skip))
            
        except KeyError:
                skip = 0
        print(form)
        # if request.GET['skip'][0]:
        #     print('SKIP FIRST {}'.format(request.GET['skip'][0]))
        if form.is_valid():
            filters = form.cleaned_data
            print('FILTERS ARE: {}'.format(filters))
            vendor = filters['vendor']
            vulner = filters['vulner']
            # try:
            #     skip = int(request.GET['skip'][0])
            #     skip += increment
            #     print('SKIP {}'.format(skip))
            #     print(type(skip))
            # except KeyError:
            #     skip = 0
        print(vendor)
        print(vulner)
        # skip += increment
        vulners = get_vulners_info(vendor, vulner, skip)
        #print(vulners['data']['search'][0]['_source']['id'])
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
