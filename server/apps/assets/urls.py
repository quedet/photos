from django.urls import path
from apps.assets import views

app_name = 'assets'

urlpatterns = [
    path('', views.AssetsListView.as_view(), name='assets-list'),
    path('favorites/', views.FavoriteAssetsView.as_view(), name='assets-favorites'),
    path('favorites/<id>/', views.MarkAssetAsFavorite.as_view(),
         name='mark-as-favorite'),
    path('assets/create/', views.CreateAssetsView.as_view(), name='assets-create'),
    path('photo/<slug>/', views.AssetDetailView.as_view(), name='assets-detail'),
    path('photo/<slug>/edit/', views.AssetEditView.as_view(), name='assets-edit')
]
