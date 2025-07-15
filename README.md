# Pin İzolatör Tespit Sistemi

Django tabanlı, 5 yönden fotoğraf analizi yapabilen pin izolatör tespit sistemi.

## 🚀 Özellikler

### 📸 Fotoğraf Yönetimi
- **5 Yönden Fotoğraf**: Sağ, Sol, Ön, Arka, Üst açılardan fotoğraf yükleme
- **GPS Koordinat Desteği**: Enlem, boylam ve yükseklik bilgisi
- **Dosya Format Desteği**: JPG, PNG, JPEG formatları
- **Fotoğraf Önizleme**: Yükleme sırasında anlık önizleme

### 🤖 Analiz Sistemi
- **Otomatik Analiz**: 5 fotoğrafın AI ile analizi
- **Durum Takibi**: Beklemede, İşleniyor, Tamamlandı, Hatalı durumları
- **Sonuç Sınıflandırması**: Sağlam, Hasarlı, Değişmeli, Belirsiz
- **Güven Skoru**: %0-100 arası güvenilirlik değeri

### 👥 Kullanıcı Yönetimi
- **Güvenli Giriş**: Kullanıcı adı/şifre ile giriş
- **Rol Tabanlı Erişim**: Operatör ve Admin rolleri
- **Kullanıcı Kayıt**: Yeni hesap oluşturma

### 📊 Raporlama ve İstatistikler
- **Detaylı İstatistikler**: Analiz durumları ve sonuçlar
- **Performans Metrikleri**: Tamamlanma ve başarı oranları
- **Geçmiş Takibi**: Tüm işlemlerin detaylı logları
- **Filtreleme ve Arama**: Gelişmiş arama özellikleri

### 🎨 Modern Arayüz
- **Responsive Tasarım**: Mobil ve masaüstü uyumlu
- **Bootstrap 5**: Modern ve kullanıcı dostu arayüz
- **Animasyonlar**: Smooth geçişler ve hover efektleri
- **Renk Kodlaması**: Durum ve sonuçlara göre renk sistemi

## 🛠️ Teknoloji Stack

- **Backend**: Django 4.2.7
- **Frontend**: Bootstrap 5, jQuery, Font Awesome
- **Veritabanı**: SQLite (Geliştirme), PostgreSQL (Production)
- **Dosya Yönetimi**: Pillow (Image Processing)
- **Form Yönetimi**: Django Crispy Forms

## 📁 Proje Yapısı

```
pin_izolator_tespit/
├── accounts/                    # Kullanıcı yönetimi
│   ├── views.py                # Giriş/Çıkış/Kayıt
│   └── urls.py                 # URL yönlendirmeleri
├── goruntu_analiz/             # Ana analiz uygulaması
│   ├── models.py              # Veritabanı modelleri
│   ├── views.py               # İş mantığı
│   ├── forms.py               # Form tanımları
│   ├── admin.py               # Admin panel ayarları
│   └── urls.py                # URL yönlendirmeleri
├── templates/                  # HTML şablonları
│   ├── base.html              # Ana şablon
│   ├── accounts/              # Kullanıcı sayfaları
│   └── goruntu_analiz/        # Analiz sayfaları
├── static/                    # Statik dosyalar
│   ├── css/style.css          # Özel CSS
│   └── js/                    # JavaScript dosyaları
├── media/                     # Yüklenen dosyalar
│   └── fotograflar/           # Fotoğraf klasörleri
├── pin_izolator_tespit/       # Ana proje ayarları
│   ├── settings.py            # Django ayarları
│   └── urls.py                # Ana URL yapılandırması
├── requirements.txt           # Python bağımlılıkları
└── manage.py                  # Django yönetim scripti
```

## 🗄️ Veritabanı Modelleri

### GoruntüAnaliz (Ana Model)
- **Temel Bilgiler**: görev_id, operator, açıklama
- **Koordinat**: enlem, boylam, yükseklik
- **Zaman**: çekim_zamanı, oluşturma_zamanı, güncelleme_zamanı
- **Fotoğraflar**: 5 yönden fotoğraf alanları
- **Analiz**: durum, sonuç, güven_skoru

### TespitDetay
- **Fotoğraf Bazlı**: Her fotoğraf için ayrı sonuç
- **Tespit Bilgileri**: nesne_tespit_edildi, hasar_tespit_edildi
- **Koordinat**: Tespit edilen nesnenin konumu

### AnalizeGecmisi
- **İşlem Takibi**: Tüm değişikliklerin kaydı
- **Kullanıcı Bilgisi**: Kim ne zaman yaptı
- **Detaylı Log**: İşlem açıklamaları

## 🚀 Kurulum

### 1. Gereksinimler
```bash
pip install -r requirements.txt
```

### 2. Veritabanı Kurulumu
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Süper Kullanıcı Oluşturma
```bash
python manage.py createsuperuser
```

### 4. Sunucu Başlatma
```bash
python manage.py runserver
```

## 👤 Varsayılan Kullanıcılar

### Admin Kullanıcı
- **Kullanıcı Adı**: admin
- **Şifre**: admin123
- **Yetki**: Tüm sistem erişimi

### Test Operatörü
- **Kullanıcı Adı**: operator1
- **Şifre**: operator123
- **Yetki**: Analiz işlemleri

## 🌐 Sayfa Yapısı

### Ana Sayfalar
- **Ana Sayfa** (`/analiz/`): Analiz listesi ve istatistikler
- **Yeni Analiz** (`/analiz/yeni/`): 5 fotoğraf yükleme formu
- **Analiz Detay** (`/analiz/detay/<id>/`): Detaylı analiz görünümü
- **Düzenleme** (`/analiz/duzenle/<id>/`): Analiz güncelleme
- **İstatistikler** (`/analiz/istatistikler/`): Sistem metrikleri

### Kullanıcı Sayfaları
- **Giriş** (`/accounts/giris/`): Sistem girişi
- **Kayıt** (`/accounts/kayit/`): Yeni hesap oluşturma
- **Admin Panel** (`/admin/`): Sistem yönetimi

## 🎯 Kullanım Senaryoları

### 1. Yeni Analiz Oluşturma
1. "Yeni Analiz" butonuna tıklayın
2. Görev ID ve koordinat bilgilerini girin
3. 5 yönden fotoğrafları yükleyin
4. "Analiz Oluştur" butonuna tıklayın

### 2. Analiz Başlatma
1. Ana sayfadan analizi seçin
2. "Analiz Başlat" butonuna tıklayın
3. Sistem otomatik olarak analiz yapar
4. Sonuçları detay sayfasında görüntüleyin

### 3. Sonuçları İnceleme
1. Analiz detay sayfasına gidin
2. 5 fotoğrafı ve sonuçları görüntüleyin
3. Güven skorunu kontrol edin
4. Gerekirse düzenleme yapın

## 📈 Gelecek Geliştirmeler

### AI/ML Entegrasyonu
- [ ] TensorFlow/PyTorch model entegrasyonu
- [ ] Gerçek nesne tespit algoritması
- [ ] Öğrenebilir model yapısı

### Harita Entegrasyonu
- [ ] Google Maps/OpenStreetMap desteği
- [ ] Koordinat üzerinde görselleştirme
- [ ] Rota planlama

### Gelişmiş Raporlama
- [ ] PDF rapor oluşturma
- [ ] Excel export
- [ ] Grafik ve chartlar
- [ ] Otomatik e-posta bildirimleri

### Mobil Uygulama
- [ ] React Native mobil app
- [ ] Offline çalışma
- [ ] Push notification

## 🐛 Bilinen Sorunlar

- [ ] Büyük dosya yükleme optimizasyonu
- [ ] Batch analiz işlemi
- [ ] Performans iyileştirmeleri

## 🤝 Katkıda Bulunma

1. Repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/YeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/YeniOzellik`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📞 İletişim

Herhangi bir sorunuz için lütfen issue açın veya iletişime geçin.

---

**Not**: Bu sistem protip amaçlı geliştirilmiştir. Production ortamında kullanmadan önce güvenlik ve performans testlerini yapınız.
