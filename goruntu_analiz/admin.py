from django.contrib import admin
from .models import GoruntüAnaliz, TespitDetay, AnalizeGecmisi


@admin.register(GoruntüAnaliz)
class GoruntüAnalizAdmin(admin.ModelAdmin):
    list_display = ['gorev_id', 'operator', 'analiz_durumu', 'tespit_sonucu', 'guven_skoru', 'olusturma_zamani']
    list_filter = ['analiz_durumu', 'tespit_sonucu', 'olusturma_zamani', 'operator']
    search_fields = ['gorev_id', 'operator__username', 'operator__first_name', 'operator__last_name']
    readonly_fields = ['olusturma_zamani', 'guncelleme_zamani', 'koordinat_str']
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('gorev_id', 'operator', 'aciklama')
        }),
        ('Konum Bilgileri', {
            'fields': ('koordinat_enlem', 'koordinat_boylam', 'yukseklik', 'cekim_zamani')
        }),
        ('Fotoğraflar', {
            'fields': ('foto_sag', 'foto_sol', 'foto_on', 'foto_arka', 'foto_ust')
        }),
        ('Analiz Sonuçları', {
            'fields': ('analiz_durumu', 'tespit_sonucu', 'guven_skoru')
        }),
        ('Zaman Bilgileri', {
            'fields': ('olusturma_zamani', 'guncelleme_zamani'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TespitDetay)
class TespitDetayAdmin(admin.ModelAdmin):
    list_display = ['goruntu_analiz', 'foto_yon', 'nesne_tespit_edildi', 'hasar_tespit_edildi', 'tespit_skoru']
    list_filter = ['foto_yon', 'nesne_tespit_edildi', 'hasar_tespit_edildi', 'olusturma_zamani']
    search_fields = ['goruntu_analiz__gorev_id']


@admin.register(AnalizeGecmisi)
class AnalizeGecmisiAdmin(admin.ModelAdmin):
    list_display = ['goruntu_analiz', 'islem', 'kullanici', 'islem_zamani']
    list_filter = ['islem', 'islem_zamani', 'kullanici']
    search_fields = ['goruntu_analiz__gorev_id', 'islem', 'kullanici__username']
    readonly_fields = ['islem_zamani']
