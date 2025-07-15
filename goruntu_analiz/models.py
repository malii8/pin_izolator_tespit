from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class GoruntüAnaliz(models.Model):
    """5 yönden çekilen fotoğrafların analiz edildiği ana model"""
    
    ANALIZ_DURUMLARI = [
        ('beklemede', 'Beklemede'),
        ('isleniyor', 'İşleniyor'),
        ('tamamlandi', 'Tamamlandı'),
        ('hatali', 'Hatalı'),
    ]
    
    TESPIT_SONUCLARI = [
        ('saglam', 'Sağlam'),
        ('hasarli', 'Hasarlı'),
        ('degismeli', 'Değişmeli'),
        ('belirsiz', 'Belirsiz'),
    ]
    
    # Temel bilgiler
    gorev_id = models.CharField('Görev ID', max_length=50, unique=True)
    operator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Operatör')
    
    # Koordinat bilgileri
    koordinat_enlem = models.DecimalField('Enlem', max_digits=10, decimal_places=8)
    koordinat_boylam = models.DecimalField('Boylam', max_digits=11, decimal_places=8)
    yukseklik = models.FloatField('Yükseklik (m)')
    
    # Zaman bilgileri
    cekim_zamani = models.DateTimeField('Çekim Zamanı')
    olusturma_zamani = models.DateTimeField('Oluşturma Zamanı', auto_now_add=True)
    guncelleme_zamani = models.DateTimeField('Güncelleme Zamanı', auto_now=True)
    
    # 5 yönden fotoğraflar
    foto_sag = models.ImageField('Sağ Fotoğraf', upload_to='fotograflar/sag/%Y/%m/')
    foto_sol = models.ImageField('Sol Fotoğraf', upload_to='fotograflar/sol/%Y/%m/')
    foto_on = models.ImageField('Ön Fotoğraf', upload_to='fotograflar/on/%Y/%m/')
    foto_arka = models.ImageField('Arka Fotoğraf', upload_to='fotograflar/arka/%Y/%m/')
    foto_ust = models.ImageField('Üst Fotoğraf', upload_to='fotograflar/ust/%Y/%m/')
    
    # Analiz durumu ve sonuç
    analiz_durumu = models.CharField('Analiz Durumu', max_length=20, choices=ANALIZ_DURUMLARI, default='beklemede')
    tespit_sonucu = models.CharField('Tespit Sonucu', max_length=30, choices=TESPIT_SONUCLARI, blank=True, null=True)
    guven_skoru = models.FloatField('Güven Skoru (%)', blank=True, null=True, help_text='0-100 arası değer')
    
    # Ek bilgiler
    aciklama = models.TextField('Açıklama', blank=True)
    
    class Meta:
        verbose_name = 'Görüntü Analiz'
        verbose_name_plural = 'Görüntü Analizleri'
        ordering = ['-olusturma_zamani']
    
    def __str__(self):
        return f"{self.gorev_id} - {self.get_analiz_durumu_display()}"
    
    def get_absolute_url(self):
        return reverse('goruntu_analiz:detay', kwargs={'pk': self.pk})
    
    @property
    def koordinat_str(self):
        """Koordinatları string olarak döndür"""
        return f"{self.koordinat_enlem}, {self.koordinat_boylam}"
    
    @property
    def tum_fotograflar_yuklendi_mi(self):
        """Tüm 5 fotoğrafın yüklenip yüklenmediğini kontrol et"""
        return all([self.foto_sag, self.foto_sol, self.foto_on, self.foto_arka, self.foto_ust])


class TespitDetay(models.Model):
    """Her bir fotoğraf için detaylı tespit sonuçları"""
    
    FOTO_YONLERI = [
        ('sag', 'Sağ'),
        ('sol', 'Sol'),
        ('on', 'Ön'),
        ('arka', 'Arka'),
        ('ust', 'Üst'),
    ]
    
    goruntu_analiz = models.ForeignKey(GoruntüAnaliz, on_delete=models.CASCADE, related_name='tespit_detaylari')
    foto_yon = models.CharField('Fotoğraf Yönü', max_length=10, choices=FOTO_YONLERI)
    
    # Tespit sonuçları
    nesne_tespit_edildi = models.BooleanField('Nesne Tespit Edildi', default=False)
    hasar_tespit_edildi = models.BooleanField('Hasar Tespit Edildi', default=False)
    tespit_skoru = models.FloatField('Tespit Skoru', blank=True, null=True)
    
    # Koordinat bilgileri (tespit edilen nesnenin fotoğraf üzerindeki konumu)
    x_koordinat = models.IntegerField('X Koordinatı', blank=True, null=True)
    y_koordinat = models.IntegerField('Y Koordinatı', blank=True, null=True)
    genislik = models.IntegerField('Genişlik', blank=True, null=True)
    yukseklik_pixel = models.IntegerField('Yükseklik (pixel)', blank=True, null=True)
    
    aciklama = models.TextField('Açıklama', blank=True)
    olusturma_zamani = models.DateTimeField('Oluşturma Zamanı', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Tespit Detayı'
        verbose_name_plural = 'Tespit Detayları'
        unique_together = ['goruntu_analiz', 'foto_yon']
    
    def __str__(self):
        return f"{self.goruntu_analiz.gorev_id} - {self.get_foto_yon_display()}"


class AnalizeGecmisi(models.Model):
    """Analiz işlemlerinin geçmişini tutar"""
    
    goruntu_analiz = models.ForeignKey(GoruntüAnaliz, on_delete=models.CASCADE, related_name='analiz_gecmisi')
    islem = models.CharField('İşlem', max_length=100)
    aciklama = models.TextField('Açıklama', blank=True)
    islem_zamani = models.DateTimeField('İşlem Zamanı', auto_now_add=True)
    kullanici = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Analiz Geçmişi'
        verbose_name_plural = 'Analiz Geçmişleri'
        ordering = ['-islem_zamani']
    
    def __str__(self):
        return f"{self.goruntu_analiz.gorev_id} - {self.islem}"
