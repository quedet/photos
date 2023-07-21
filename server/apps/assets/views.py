from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
import http
from apps.assets.forms import ImageForm
from apps.assets.models import Image, Favorite, Trash
from guardian.shortcuts import get_objects_for_user
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from turbo_response import TurboStreamResponse, TurboStream


class AssetsListView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/assets/index.html'
    # login_url = reverse('accounts:login')
    raise_exception = False

    def get(self, request, *args, **kwargs):
        photos = get_objects_for_user(
            request.user, 'assets.view_image', Image, any_perm=True, with_superuser=False)

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


class AssetDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/assets/detail.html'

    def get(self, request, *args, **kwargs):
        all_photos = get_objects_for_user(
            request.user, 'assets.view_image', Image, any_perm=True)
        paginator = Paginator(all_photos, 1)

        current_photo = get_object_or_404(Image, slug=kwargs['slug'])
        photos_ids = [item.id for item in all_photos]
        current_index = photos_ids.index(current_photo.id) + 1

        # print(f"All Photos IDS: {photos_ids}")
        # print(f"Current Photo ID: {current_photo.id}")
        # print(f"Current Photo Index: {current_index}")

        try:
            current_photo = paginator.page(current_index)
        except PageNotAnInteger:
            current_photo = paginator.page(1)
        except EmptyPage:
            current_photo = paginator.page(paginator.num_pages)

        next_photo = None
        next_photo_index = None
        next_photo_id = None

        if current_photo.has_next():
            next_photo_index = current_photo.next_page_number() - 1
            next_photo_id = photos_ids[next_photo_index]

            if next_photo_id in photos_ids:
                next_photo = Image.objects.get(id=next_photo_id)

        previous_photo = None
        previous_photo_index = None
        previous_photo_id = None

        if current_photo.has_previous():
            previous_photo_index = current_photo.previous_page_number() - 1
            previous_photo_id = photos_ids[previous_photo_index]

            if previous_photo_id in photos_ids:
                previous_photo = Image.objects.get(id=previous_photo_id)

        # print("Next Photo")
        # print(next_photo)
        # print("Previous Photo")
        # print(previous_photo)

        return self.render_to_response({
            'photo': current_photo.object_list[0],
            'next_photo': next_photo,
            'previous_photo': previous_photo
        })


class AssetEditView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/assets/edit.html'

    def get(self, request, *args, **kwargs):
        photo = get_object_or_404(Image, slug=kwargs['slug'])
        return self.render_to_response({
            'photo': photo
        })


class FavoriteAssetsView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/assets/favorites/index.html'

    def get(self, request, *args, **kwargs):
        photos = get_objects_for_user(
            request.user, 'assets.view_favorite', Favorite, any_perm=True, with_superuser=False)
        return self.render_to_response({
            'photos': photos
        })


class FavoriteAssetDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/assets/favorites/detail.html'

    def get(self, request, *args, **kwargs):
        all_photos = get_objects_for_user(
            request.user, 'assets.view_favorite', Favorite, any_perm=True)
        paginator = Paginator(all_photos, 1)

        current_photo = get_object_or_404(Favorite, image__slug=kwargs['slug'])
        photos_ids = [item.image.id for item in all_photos]
        current_index = photos_ids.index(current_photo.image.id) + 1

        try:
            current_photo = paginator.page(current_index)
        except PageNotAnInteger:
            current_photo = paginator.page(1)
        except EmptyPage:
            current_photo = paginator.page(paginator.num_pages)

        next_photo = None
        next_photo_index = None
        next_photo_id = None

        if current_photo.has_next():
            next_photo_index = current_photo.next_page_number() - 1
            next_photo_id = photos_ids[next_photo_index]

            if next_photo_id in photos_ids:
                next_photo = Favorite.objects.get(image_id=next_photo_id)

        previous_photo = None
        previous_photo_index = None
        previous_photo_id = None

        if current_photo.has_previous():
            previous_photo_index = current_photo.previous_page_number() - 1
            previous_photo_id = photos_ids[previous_photo_index]

            if previous_photo_id in photos_ids:
                previous_photo = Favorite.objects.get(
                    image_id=previous_photo_id)

        return self.render_to_response({
            'photo': current_photo.object_list[0].image,
            'next_photo': next_photo,
            'previous_photo': previous_photo
        })


class MarkAssetAsFavorite(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        image = get_object_or_404(Image, id=kwargs['id'])
        favorite, created = Favorite.objects.get_or_create(
            owner=request.user, image=image)
        action = "unmark"

        if not created:
            favorite.delete()
            action = "mark"

        return TurboStreamResponse([
            TurboStream(f"asset--{kwargs['id']}--button").update.template("components/blocks/favorite.html", {
                "action": action
            })
        ])


class TrashAssetsView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/assets/trash/index.html'

    def get(self, request, *args, **kwargs):
        photos = get_objects_for_user(
            request.user, 'assets.view_trash', Trash, any_perm=True, with_superuser=False)
        return self.render_to_response({
            'photos': photos
        })


class TrashAssetDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/assets/trash/detail.html'

    def get(self, request, *args, **kwargs):
        all_photos = get_objects_for_user(
            request.user, 'assets.view_trash', Trash, any_perm=True)
        paginator = Paginator(all_photos, 1)

        current_photo = get_object_or_404(Trash, image__slug=kwargs['slug'])
        photos_ids = [item.image.id for item in all_photos]
        current_index = photos_ids.index(current_photo.image.id) + 1

        try:
            current_photo = paginator.page(current_index)
        except PageNotAnInteger:
            current_photo = paginator.page(1)
        except EmptyPage:
            current_photo = paginator.page(paginator.num_pages)

        next_photo = None
        next_photo_index = None
        next_photo_id = None

        if current_photo.has_next():
            next_photo_index = current_photo.next_page_number() - 1
            next_photo_id = photos_ids[next_photo_index]

            if next_photo_id in photos_ids:
                next_photo = Trash.objects.get(image_id=next_photo_id)

        previous_photo = None
        previous_photo_index = None
        previous_photo_id = None

        if current_photo.has_previous():
            previous_photo_index = current_photo.previous_page_number() - 1
            previous_photo_id = photos_ids[previous_photo_index]

            if previous_photo_id in photos_ids:
                previous_photo = Trash.objects.get(image_id=previous_photo_id)

        return self.render_to_response({
            'photo': current_photo.object_list[0].image,
            'next_photo': next_photo,
            'previous_photo': previous_photo
        })


class MarkAssetAsTrashed(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        image = get_object_or_404(Image, id=kwargs['id'])
        trash, created = Trash.objects.get_or_create(
            owner=request.user, image=image)
        action = "restore"

        if not created:
            trash.delete()
            action = "delete"

        return TurboStreamResponse([
            TurboStream(f"asset--{kwargs['id']}--button").update.template("components/blocks/favorite.html", {
                "action": action
            })
        ])
