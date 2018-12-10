from django.urls import path

from .views import *

urlpatterns = [
    path('', VulnersListView.as_view(), name='vulners'),
]
