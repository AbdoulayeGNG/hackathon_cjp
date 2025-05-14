from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from reports.models import Report
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
import json
from django.core.paginator import Paginator
from django.db.models import Q

User = get_user_model()

def is_admin(user):
    return user.is_authenticated and user.is_staff

def home(request):
    context = {
        'recent_reports': Report.objects.all().order_by('-created_at')[:6],
        'total_reports': Report.objects.count(),
        'resolved_reports': Report.objects.filter(status='resolved').count(),
        'total_users': get_user_model().objects.count(),
    }
    return render(request, 'index.html', context)

@user_passes_test(lambda u: u.is_staff)
def dashboard(request):
    # Statistiques générales
    total_reports = Report.objects.count()
    pending_reports = Report.objects.filter(status='pending').count()
    in_progress_reports = Report.objects.filter(status='in_progress').count()
    resolved_reports = Report.objects.filter(status='resolved').count()
    
    # Statistiques sur 7 derniers jours
    last_week = timezone.now() - timedelta(days=7)
    daily_stats = (
        Report.objects
        .filter(created_at__gte=last_week)
        .values('created_at__date')  # Changed from extra() to values()
        .annotate(count=Count('id'))
        .order_by('created_at__date')
    )
    
    # Convertir les dates en format JSON-compatible
    daily_stats_json = [
        {
            'day': item['created_at__date'].isoformat(),  # Using isoformat() for dates
            'count': item['count']
        }
        for item in daily_stats
    ]
    
    # Statistiques par catégorie
    categories_stats = (
        Report.objects
        .values('category')
        .annotate(count=Count('id'))
        .order_by('category')
    )
    
    # Préparer les données pour les graphiques
    categories_data = [
        {
            'category': dict(Report.CATEGORY_CHOICES).get(stat['category'], stat['category']),
            'count': stat['count']
        }
        for stat in categories_stats
    ]

    context = {
        'total_reports': total_reports,
        'pending_reports': pending_reports,
        'in_progress_reports': in_progress_reports,
        'resolved_reports': resolved_reports,
        'reports': Report.objects.select_related('user').order_by('-created_at')[:10],
        'daily_stats': json.dumps(daily_stats_json),
        'categories_stats': json.dumps(categories_data)
    }
    
    return render(request, 'dashboard/dashboard.html', context)

@user_passes_test(lambda u: u.is_staff)
def update_report_status(request, report_id):
    if request.method == 'POST':
        report = get_object_or_404(Report, id=report_id)
        new_status = request.POST.get('status')
        if new_status in ['pending', 'in_progress', 'resolved']:
            report.status = new_status
            report.save()
            messages.success(request, f'Statut du signalement #{report.id} mis à jour.')
        else:
            messages.error(request, 'Statut invalide.')
    return redirect('dashboard:dashboard')

@user_passes_test(lambda u: u.is_staff)
def manage_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    
    if request.method == "POST":
        new_status = request.POST.get('status')
        if new_status in ['pending', 'in_progress', 'resolved']:
            report.status = new_status
            report.save()
            messages.success(request, f'Le statut du signalement #{report.id} a été mis à jour.')
            return redirect('dashboard:admin_dashboard')
        else:
            messages.error(request, 'Statut invalide.')
    
    # Récupérer d'autres signalements pour le contexte
    all_reports = Report.objects.select_related('user').order_by('-created_at')
    
    context = {
        'report': report,
        'all_reports': all_reports,
        'status_choices': Report.STATUS_CHOICES,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    # Get all reports with related user data
    reports = Report.objects.select_related('user').order_by('-created_at')
    
    context = {
        'reports': reports,  # Changed from all_reports to reports for consistency
        'pending_reports': reports.filter(status='pending').count(),
        'in_progress_reports': reports.filter(status='in_progress').count(),
        'resolved_reports': reports.filter(status='resolved').count(),
        'total_reports': reports.count(),
        'status_choices': Report.STATUS_CHOICES,  # Add status choices for form
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser)
def admin_list(request):
    # Recherche
    query = request.GET.get('q', '')
    admins = User.objects.filter(is_staff=True)
    
    if query:
        admins = admins.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(admins.order_by('-date_joined'), 10)
    page = request.GET.get('page')
    admins = paginator.get_page(page)
    
    return render(request, 'dashboard/admin/list.html', {'admins': admins, 'query': query})

@user_passes_test(lambda u: u.is_superuser)
def admin_create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        if password != password_confirm:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
            return redirect('dashboard:admin_create')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ce nom d\'utilisateur existe déjà.')
            return redirect('dashboard:admin_create')
            
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True
        )
        messages.success(request, f'Administrateur {username} créé avec succès.')
        return redirect('dashboard:admin_list')
        
    return render(request, 'dashboard/admin/create.html')

@user_passes_test(lambda u: u.is_superuser)
def admin_edit(request, admin_id):
    admin = get_object_or_404(User, id=admin_id, is_staff=True)
    
    if request.method == 'POST':
        admin.first_name = request.POST.get('first_name', '')
        admin.last_name = request.POST.get('last_name', '')
        admin.email = request.POST.get('email', '')
        
        if request.POST.get('password'):
            admin.set_password(request.POST.get('password'))
            
        admin.save()
        messages.success(request, f'Administrateur {admin.username} modifié avec succès.')
        return redirect('dashboard:admin_list')
        
    return render(request, 'dashboard/admin/edit.html', {'admin': admin})

@user_passes_test(lambda u: u.is_superuser)
def admin_delete(request, admin_id):
    admin = get_object_or_404(User, id=admin_id, is_staff=True)
    
    if request.method == 'POST':
        if admin.is_superuser:
            messages.error(request, 'Impossible de supprimer un super-administrateur.')
        else:
            username = admin.username
            admin.is_staff = False
            admin.save()
            messages.success(request, f'Les droits d\'administrateur de {username} ont été révoqués.')
        return redirect('dashboard:admin_list')
        
    return render(request, 'dashboard/admin/delete.html', {'admin': admin})
