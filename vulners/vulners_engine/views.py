from django.shortcuts import render
from .forms import FilterForm
from django.views import generic

import requests
import json


def get_vulners_info(search_param):
    params = {
        'query': 'type:{}'.format(search_param)

    }
    vulners = requests.get(
        'https://vulners.com/api/v3/search/lucene/', params=params).json()
    return vulners


class VulnersListView(generic.ListView):
    # template_name = 'vulners_engine/vulners_list.html'


    def get(self, request):
        form = FilterForm()
        vulners = get_vulners_info('cve')
        print(vulners)
        return render(request, 'vulners_list.html', context={'form': form, 'vulners': vulners})

    # def post(self, request):
    #     bound_form = PostForm(request.POST)
    #     if bound_form.is_valid():
    #         new_post = bound_form.save()
    #         return redirect(new_post)
    #     return render(request, 'blog/post_create.html', context={'form':bound_form})
