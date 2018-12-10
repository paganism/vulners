from django.shortcuts import render
from .forms import FilterForm
from django.views import generic

import requests
import json


def get_vulners_info(vendor, vulner):
    params = {
        'query': 'type:{}'.format(vendor),
        'id': vulner

    }
    vulners = requests.get(
        'https://vulners.com/api/v3/search/lucene/', params=params).json()

    return  vulners #json.loads(vulners)


class VulnersListView(generic.ListView):
    # template_name = 'vulners_engine/vulners_list.html'


    def get(self, request):
        form = FilterForm(request.GET or None)
        vendor = None
        vulner = None
        print(form)
        if form.is_valid():
            filters = form.cleaned_data
            print('FILTERS ARE: {}'.format(filters))
            vendor = filters['vendor']
            vulner = filters['vulner']
        print(vendor)
        print(vulner)
        vulners = get_vulners_info(vendor, vulner)
        print(vulners['data']['search'][0]['_source']['id'])
        vln_lst = []
        for i in vulners['data']['search']:
            vln_lst.append(i['_source'])
        #print(vln_lst[0])
        return render(request, 'vulners_list.html', context={'form': form, 'vulners_list': vln_lst})

    # def post(self, request):
    #     bound_form = PostForm(request.POST)
    #     if bound_form.is_valid():
    #         new_post = bound_form.save()
    #         return redirect(new_post)
    #     return render(request, 'blog/post_create.html', context={'form':bound_form})
