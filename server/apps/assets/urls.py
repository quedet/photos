from django.urls import path
from apps.assets import views

app_name = 'assets'

urlpatterns = [
    path('', views.AssetsListView.as_view(), name='assets-list'),
    path('favorites/', views.FavoriteAssetsView.as_view(), name='assets-favorites'),
    path('favorites/<int:id>/', views.MarkAssetAsFavorite.as_view(),
         name='mark-as-favorite'),
    path('favorites/<slug:slug>/', views.FavoriteAssetDetailView.as_view(),
         name='assets-favorite-detail'),
    path('trash/', views.TrashAssetsView.as_view(), name='assets-trash'),
    path('trash/<int:id>/', views.MarkAssetAsTrashed.as_view(),
         name='mark-as-deleted'),
    path('trash/<slug:slug>/', views.TrashAssetDetailView.as_view(),
         name='assets-trash-detail'),
    path('assets/create/', views.CreateAssetsView.as_view(), name='assets-create'),
    path('photo/<slug>/', views.AssetDetailView.as_view(), name='assets-detail'),
    path('photo/<slug>/edit/', views.AssetEditView.as_view(), name='assets-edit')
]
