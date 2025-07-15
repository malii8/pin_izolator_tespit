from django import forms
from django.core.exceptions import ValidationError
from .models import GoruntüAnaliz
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML


class GoruntüAnalizForm(forms.ModelForm):
    """Yeni görüntü analizi oluşturma formu"""
    
    class Meta:
        model = GoruntüAnaliz
        fields = [
            'gorev_id', 'koordinat_enlem', 'koordinat_boylam', 'yukseklik',
            'cekim_zamani', 'foto_sag', 'foto_sol', 'foto_on', 'foto_arka',
            'foto_ust', 'aciklama'
        ]
        widgets = {
            'cekim_zamani': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'aciklama': forms.Textarea(attrs={'rows': 3}),
            'koordinat_enlem': forms.NumberInput(attrs={'step': '0.00000001'}),
            'koordinat_boylam': forms.NumberInput(attrs={'step': '0.00000001'}),
            'yukseklik': forms.NumberInput(attrs={'step': '0.1'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('gorev_id', css_class='form-group col-md-6 mb-3'),
                Column('cekim_zamani', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('koordinat_enlem', css_class='form-group col-md-4 mb-3'),
                Column('koordinat_boylam', css_class='form-group col-md-4 mb-3'),
                Column('yukseklik', css_class='form-group col-md-4 mb-3'),
            ),
            HTML('<h5 class="mt-4 mb-3">5 Yönden Fotoğraflar</h5>'),
            Row(
                Column('foto_sag', css_class='form-group col-md-6 mb-3'),
                Column('foto_sol', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('foto_on', css_class='form-group col-md-4 mb-3'),
                Column('foto_arka', css_class='form-group col-md-4 mb-3'),
                Column('foto_ust', css_class='form-group col-md-4 mb-3'),
            ),
            'aciklama',
            Submit('submit', 'Analiz Oluştur', css_class='btn btn-primary btn-lg mt-3')
        )
        
        # Tüm alanlar zorunlu
        for field in self.fields:
            if field != 'aciklama':
                self.fields[field].required = True
        
        # Yardım metinleri
        self.fields['gorev_id'].help_text = 'Benzersiz görev kimliği'
        self.fields['koordinat_enlem'].help_text = 'Enlem (-90 ile 90 arası)'
        self.fields['koordinat_boylam'].help_text = 'Boylam (-180 ile 180 arası)'
        self.fields['yukseklik'].help_text = 'Metre cinsinden yükseklik'
    
    def clean_koordinat_enlem(self):
        enlem = self.cleaned_data['koordinat_enlem']
        if enlem < -90 or enlem > 90:
            raise ValidationError('Enlem -90 ile 90 derece arasında olmalıdır.')
        return enlem
    
    def clean_koordinat_boylam(self):
        boylam = self.cleaned_data['koordinat_boylam']
        if boylam < -180 or boylam > 180:
            raise ValidationError('Boylam -180 ile 180 derece arasında olmalıdır.')
        return boylam
    
    def clean_yukseklik(self):
        yukseklik = self.cleaned_data['yukseklik']
        if yukseklik < 0:
            raise ValidationError('Yükseklik negatif olamaz.')
        return yukseklik


class GoruntüDuzenleForm(forms.ModelForm):
    """Mevcut görüntü analizi düzenleme formu"""
    
    class Meta:
        model = GoruntüAnaliz
        fields = [
            'gorev_id', 'koordinat_enlem', 'koordinat_boylam', 'yukseklik',
            'cekim_zamani', 'foto_sag', 'foto_sol', 'foto_on', 'foto_arka',
            'foto_ust', 'analiz_durumu', 'tespit_sonucu', 'guven_skoru',
            'aciklama'
        ]
        widgets = {
            'cekim_zamani': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'aciklama': forms.Textarea(attrs={'rows': 3}),
            'koordinat_enlem': forms.NumberInput(attrs={'step': '0.00000001'}),
            'koordinat_boylam': forms.NumberInput(attrs={'step': '0.00000001'}),
            'yukseklik': forms.NumberInput(attrs={'step': '0.1'}),
            'guven_skoru': forms.NumberInput(attrs={'step': '0.1', 'min': '0', 'max': '100'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('gorev_id', css_class='form-group col-md-6 mb-3'),
                Column('cekim_zamani', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('koordinat_enlem', css_class='form-group col-md-4 mb-3'),
                Column('koordinat_boylam', css_class='form-group col-md-4 mb-3'),
                Column('yukseklik', css_class='form-group col-md-4 mb-3'),
            ),
            HTML('<h5 class="mt-4 mb-3">5 Yönden Fotoğraflar</h5>'),
            Row(
                Column('foto_sag', css_class='form-group col-md-6 mb-3'),
                Column('foto_sol', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('foto_on', css_class='form-group col-md-4 mb-3'),
                Column('foto_arka', css_class='form-group col-md-4 mb-3'),
                Column('foto_ust', css_class='form-group col-md-4 mb-3'),
            ),
            HTML('<h5 class="mt-4 mb-3">Analiz Sonuçları</h5>'),
            Row(
                Column('analiz_durumu', css_class='form-group col-md-4 mb-3'),
                Column('tespit_sonucu', css_class='form-group col-md-4 mb-3'),
                Column('guven_skoru', css_class='form-group col-md-4 mb-3'),
            ),
            'aciklama',
            Submit('submit', 'Güncelle', css_class='btn btn-success btn-lg mt-3')
        )


class AnalizAramaForm(forms.Form):
    """Analiz arama formu"""
    
    arama = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Görev ID, operatör adı...',
            'class': 'form-control'
        })
    )
    
    durum = forms.ChoiceField(
        choices=[('', 'Tüm Durumlar')] + GoruntüAnaliz.ANALIZ_DURUMLARI,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    sonuc = forms.ChoiceField(
        choices=[('', 'Tüm Sonuçlar')] + GoruntüAnaliz.TESPIT_SONUCLARI,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
