from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import UtilisateurCreationForm, UserProfileForm  # Add UserProfileForm here
from django.utils import timezone
import random
from datetime import timedelta

def register(request):
    if request.method == 'POST':
        form = UtilisateurCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.otp = str(random.randint(100000, 999999))
            user.otp_created_at = timezone.now()
            user.save()
            # Stocker l'ID utilisateur dans la session
            request.session['user_id'] = user.id
            # Ici, vous devrez implémenter l'envoi d'email avec l'OTP
            messages.success(request, 'Compte créé avec succès! Veuillez vérifier votre email pour le code OTP.')
            return redirect('utilisateurs:verify_otp')
    else:
        form = UtilisateurCreationForm()
    return render(request, 'utilisateurs/register.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user = request.session.get('user_id', None)
        if user:
            user = User.objects.get(id=user)
            if user.otp == otp and user.otp_created_at + timedelta(minutes=10) > timezone.now():
                user.is_verified = True
                user.save()
                login(request, user)
                messages.success(request, 'Votre compte a été vérifié avec succès!')
                return redirect('dashboard:home')
            else:
                messages.error(request, 'Code OTP invalide ou expiré!')
        else:
            messages.error(request, 'Session expirée. Veuillez vous réinscrire.')
            return redirect('utilisateurs:register')
    return render(request, 'utilisateurs/verify_otp.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        remember = request.POST.get('remember', False)
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            if not remember:
                request.session.set_expiry(0)
            messages.success(request, 'Connexion réussie!')
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Email ou mot de passe incorrect.')
    
    return render(request, 'utilisateurs/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('dashboard:home')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'utilisateurs/password_reset.html'
    email_template_name = 'utilisateurs/password_reset_email.html'
    success_url = reverse_lazy('utilisateurs:password_reset_done')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès!')
            return redirect('utilisateurs:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user,
        'total_reports': request.user.report_set.count(),
        'resolved_reports': request.user.report_set.filter(status='resolved').count(),
    }
    return render(request, 'utilisateurs/profile.html', context)