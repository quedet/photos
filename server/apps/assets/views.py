from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

# Create your views here.


class AssetsListView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/assets/index.html'
    # login_url = reverse('accounts:login')
    raise_exception = False
