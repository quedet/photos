from django.urls import path
from apps.assets import views

app_name = 'assets'

urlpatterns = [
    path('', views.AssetsListView.as_view(), name='assets-list')
]
