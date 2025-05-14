from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from reports.models import Report
from django.contrib.auth import get_user_model

def home(request):
    context = {
        'recent_reports': Report.objects.all().order_by('-created_at')[:6],
        'total_reports': Report.objects.count(),
        'resolved_reports': Report.objects.filter(status='resolved').count(),
        'total_users': get_user_model().objects.count(),
    }
    return render(request, 'index.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    context = {
        'all_reports': Report.objects.all().order_by('-created_at'),
        'pending_reports': Report.objects.filter(status='pending').count(),
        'in_progress_reports': Report.objects.filter(status='in_progress').count(),
        'resolved_reports': Report.objects.filter(status='resolved').count(),
    }
    return render(request, 'dashboard/admin_dashboard.html', context)
