from django.urls import path
from apps.assets import views

app_name = 'assets'

urlpatterns = [
    path('', views.AssetsListView.as_view(), name='assets-list'),
    path('assets/create/', views.CreateAssetsView.as_view(), name='assets-create')
]
