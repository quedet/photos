from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
import http
from apps.assets.forms import ImageForm
from apps.assets.models import Image
from guardian.shortcuts import get_objects_for_user
# Create your views here.


class AssetsListView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/assets/index.html'
    # login_url = reverse('accounts:login')
    raise_exception = False

    def get(self, request, *args, **kwargs):
        photos = get_objects_for_user(
            request.user, 'assets.view_image', Image, any_perm=True)
        return self.render_to_response({
            'photos': photos
        })


class CreateAssetsView(LoginRequiredMixin, FormView):
    template_name = 'pages/assets/form/form.html'
    form_class = ImageForm
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        response.status_code = http.HTTPStatus.OK
        image = form.save(commit=False)
        image.owner = self.request.user
        image.save()
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = http.HTTPStatus.UNPROCESSABLE_ENTITY
        return response
