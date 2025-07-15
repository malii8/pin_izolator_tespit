from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import GoruntüAnaliz, TespitDetay, AnalizeGecmisi
from .forms import GoruntüAnalizForm, GoruntüDuzenleForm


@login_required
def anasayfa(request):
    """Ana sayfa - Son analizlerin listesi"""
    analizler = GoruntüAnaliz.objects.select_related('operator').all()
    
    # Arama fonksiyonu
    arama = request.GET.get('arama')
    if arama:
        analizler = analizler.filter(
            Q(gorev_id__icontains=arama) |
            Q(operator__username__icontains=arama) |
            Q(operator__first_name__icontains=arama) |
            Q(operator__last_name__icontains=arama)
        )
    
    # Durum filtresi
    durum = request.GET.get('durum')
    if durum:
        analizler = analizler.filter(analiz_durumu=durum)
    
    # Sayfalama
    paginator = Paginator(analizler, 10)
    sayfa = request.GET.get('sayfa')
    analizler = paginator.get_page(sayfa)
    
    # İstatistikler
    toplam_analiz = GoruntüAnaliz.objects.count()
    beklemede = GoruntüAnaliz.objects.filter(analiz_durumu='beklemede').count()
    tamamlandi = GoruntüAnaliz.objects.filter(analiz_durumu='tamamlandi').count()
    hasarli = GoruntüAnaliz.objects.filter(tespit_sonucu='hasarli').count()
    
    context = {
        'analizler': analizler,
        'toplam_analiz': toplam_analiz,
        'beklemede': beklemede,
        'tamamlandi': tamamlandi,
        'hasarli': hasarli,
        'arama': arama,
        'durum': durum,
        'title': 'Ana Sayfa - Pin İzolatör Tespit Sistemi'
    }
    
    return render(request, 'goruntu_analiz/anasayfa.html', context)


@login_required
def yeni_analiz(request):
    """Yeni analiz oluşturma sayfası"""
    if request.method == 'POST':
        form = GoruntüAnalizForm(request.POST, request.FILES)
        if form.is_valid():
            analiz = form.save(commit=False)
            analiz.operator = request.user
            analiz.save()
            
            # Analiz geçmişine kaydet
            AnalizeGecmisi.objects.create(
                goruntu_analiz=analiz,
                islem='Yeni analiz oluşturuldu',
                kullanici=request.user
            )
            
            messages.success(request, f'Görev {analiz.gorev_id} başarıyla oluşturuldu!')
            return redirect('goruntu_analiz:detay', pk=analiz.pk)
    else:
        form = GoruntüAnalizForm()
    
    context = {
        'form': form,
        'title': 'Yeni Analiz Oluştur'
    }
    return render(request, 'goruntu_analiz/yeni_analiz.html', context)


@login_required
def analiz_detay(request, pk):
    """Analiz detay sayfası"""
    analiz = get_object_or_404(GoruntüAnaliz, pk=pk)
    tespit_detaylari = TespitDetay.objects.filter(goruntu_analiz=analiz)
    gecmis = AnalizeGecmisi.objects.filter(goruntu_analiz=analiz)
    
    # Fotoğraf listesi
    fotograflar = []
    if analiz.foto_sag:
        fotograflar.append({'yon': 'Sağ', 'url': analiz.foto_sag.url})
    if analiz.foto_sol:
        fotograflar.append({'yon': 'Sol', 'url': analiz.foto_sol.url})
    if analiz.foto_on:
        fotograflar.append({'yon': 'Ön', 'url': analiz.foto_on.url})
    if analiz.foto_arka:
        fotograflar.append({'yon': 'Arka', 'url': analiz.foto_arka.url})
    if analiz.foto_ust:
        fotograflar.append({'yon': 'Üst', 'url': analiz.foto_ust.url})
    
    context = {
        'analiz': analiz,
        'tespit_detaylari': tespit_detaylari,
        'gecmis': gecmis,
        'fotograflar': fotograflar,
        'title': f'Analiz Detayı - {analiz.gorev_id}'
    }
    return render(request, 'goruntu_analiz/detay.html', context)


@login_required
def analiz_duzenle(request, pk):
    """Analiz düzenleme sayfası"""
    analiz = get_object_or_404(GoruntüAnaliz, pk=pk)
    
    if request.method == 'POST':
        form = GoruntüDuzenleForm(request.POST, request.FILES, instance=analiz)
        if form.is_valid():
            form.save()
            
            # Analiz geçmişine kaydet
            AnalizeGecmisi.objects.create(
                goruntu_analiz=analiz,
                islem='Analiz güncellendi',
                kullanici=request.user
            )
            
            messages.success(request, 'Analiz başarıyla güncellendi!')
            return redirect('goruntu_analiz:detay', pk=analiz.pk)
    else:
        form = GoruntüDuzenleForm(instance=analiz)
    
    context = {
        'form': form,
        'analiz': analiz,
        'title': f'Analiz Düzenle - {analiz.gorev_id}'
    }
    return render(request, 'goruntu_analiz/duzenle.html', context)


@login_required
def analiz_sil(request, pk):
    """Analiz silme işlemi"""
    analiz = get_object_or_404(GoruntüAnaliz, pk=pk)
    
    if request.method == 'POST':
        gorev_id = analiz.gorev_id
        analiz.delete()
        messages.success(request, f'Görev {gorev_id} başarıyla silindi!')
        return redirect('goruntu_analiz:anasayfa')
    
    context = {
        'analiz': analiz,
        'title': f'Analiz Sil - {analiz.gorev_id}'
    }
    return render(request, 'goruntu_analiz/sil.html', context)


@login_required
def analiz_baslat(request, pk):
    """Analiz işlemini başlat"""
    if request.method == 'POST':
        analiz = get_object_or_404(GoruntüAnaliz, pk=pk)
        
        if analiz.tum_fotograflar_yuklendi_mi:
            analiz.analiz_durumu = 'isleniyor'
            analiz.save()
            
            # Analiz geçmişine kaydet
            AnalizeGecmisi.objects.create(
                goruntu_analiz=analiz,
                islem='Analiz işlemi başlatıldı',
                kullanici=request.user
            )
            
            # Burada makine öğrenmesi modeli çağrılabilir
            # simdilik basit bir sonuç atayalım
            import random
            analiz.tespit_sonucu = random.choice(['saglam', 'hasarli', 'degismeli'])
            analiz.guven_skoru = random.uniform(70, 95)
            analiz.analiz_durumu = 'tamamlandi'
            analiz.save()
            
            # Analiz geçmişine kaydet
            AnalizeGecmisi.objects.create(
                goruntu_analiz=analiz,
                islem=f'Analiz tamamlandı - Sonuç: {analiz.get_tespit_sonucu_display()}',
                kullanici=request.user
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Analiz başarıyla tamamlandı!',
                'sonuc': analiz.get_tespit_sonucu_display(),
                'skor': analiz.guven_skoru
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Tüm fotoğraflar yüklenmeden analiz başlatılamaz!'
            })
    
    return JsonResponse({'success': False, 'message': 'Geçersiz istek!'})


@login_required
def istatistikler(request):
    """İstatistik sayfası"""
    # Genel istatistikler
    toplam_analiz = GoruntüAnaliz.objects.count()
    beklemede = GoruntüAnaliz.objects.filter(analiz_durumu='beklemede').count()
    isleniyor = GoruntüAnaliz.objects.filter(analiz_durumu='isleniyor').count()
    tamamlandi = GoruntüAnaliz.objects.filter(analiz_durumu='tamamlandi').count()
    hatali = GoruntüAnaliz.objects.filter(analiz_durumu='hatali').count()
    
    # Tespit sonuçları
    saglam = GoruntüAnaliz.objects.filter(tespit_sonucu='saglam').count()
    hasarli = GoruntüAnaliz.objects.filter(tespit_sonucu='hasarli').count()
    degismeli = GoruntüAnaliz.objects.filter(tespit_sonucu='degismeli').count()
    belirsiz = GoruntüAnaliz.objects.filter(tespit_sonucu='belirsiz').count()
    
    # Operatör istatistikleri
    operatorler = GoruntüAnaliz.objects.values('operator__username').distinct().count()
    
    context = {
        'toplam_analiz': toplam_analiz,
        'beklemede': beklemede,
        'isleniyor': isleniyor,
        'tamamlandi': tamamlandi,
        'hatali': hatali,
        'saglam': saglam,
        'hasarli': hasarli,
        'degismeli': degismeli,
        'belirsiz': belirsiz,
        'operatorler': operatorler,
        'title': 'İstatistikler'
    }
    
    return render(request, 'goruntu_analiz/istatistikler.html', context)
