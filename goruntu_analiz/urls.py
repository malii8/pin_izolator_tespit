from django.urls import path
from . import views

app_name = 'goruntu_analiz'

urlpatterns = [
    path('', views.anasayfa, name='anasayfa'),
    path('yeni/', views.yeni_analiz, name='yeni_analiz'),
    path('detay/<int:pk>/', views.analiz_detay, name='detay'),
    path('duzenle/<int:pk>/', views.analiz_duzenle, name='duzenle'),
    path('sil/<int:pk>/', views.analiz_sil, name='sil'),
    path('baslat/<int:pk>/', views.analiz_baslat, name='baslat'),
    path('istatistikler/', views.istatistikler, name='istatistikler'),
]
