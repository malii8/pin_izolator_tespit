from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('giris/', views.KullaniciGirisView.as_view(), name='login'),
    path('cikis/', views.KullaniciCikisView.as_view(), name='logout'),
    path('kayit/', views.kayit_ol, name='kayit'),
]
