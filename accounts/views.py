from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy


class KullaniciGirisView(LoginView):
    """Kullanıcı giriş sayfası"""
    template_name = 'accounts/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pin İzolatör Tespit Sistemi - Giriş'
        return context


class KullaniciCikisView(LogoutView):
    """Kullanıcı çıkış işlemi"""
    next_page = reverse_lazy('accounts:login')


def kayit_ol(request):
    """Yeni kullanıcı kayıt sayfası"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} kullanıcısı başarıyla oluşturuldu!')
            return redirect('accounts:login')
    else:
        form = UserCreationForm()
    
    context = {
        'form': form,
        'title': 'Yeni Kullanıcı Kayıt'
    }
    return render(request, 'accounts/kayit.html', context)
