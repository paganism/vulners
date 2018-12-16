from django.urls import path

from .views import VulnersListView

urlpatterns = [
    path('', VulnersListView.as_view(), name='vulners'),
]
