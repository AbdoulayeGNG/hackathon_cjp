from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Report
from .forms import ReportForm

@login_required
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        print("Données POST reçues:", request.POST) # Debug
        print("Fichiers reçus:", request.FILES) # Debug
        
        if form.is_valid():
            try:
                report = form.save(commit=False)
                report.user = request.user
                report.save()
                messages.success(request, 'Signalement créé avec succès!')
                return redirect('reports:detail', pk=report.pk)
            except Exception as e:
                print("Erreur lors de la sauvegarde:", str(e)) # Debug
                messages.error(request, f'Erreur lors de la création: {str(e)}')
        else:
            print("Erreurs du formulaire:", form.errors) # Debug
            messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = ReportForm()
    
    return render(request, 'reports/create_report.html', {'form': form})

@login_required
def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    print(f"Debug - Coordonnées du signalement : lat={report.location_lat}, lng={report.location_lng}")
    return render(request, 'reports/report_detail.html', {'report': report})

def report_list(request):
    reports = Report.objects.all()
    return render(request, 'reports/report_list.html', {'reports': reports})

@login_required
def update_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    print(f"Debug - Coordinates: lat={report.location_lat}, lng={report.location_lng}")  # Debug line
    
    # Vérifier si l'utilisateur a le droit de modifier ce signalement
    if not (request.user.is_staff or request.user == report.user):
        raise PermissionDenied
    
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le signalement a été modifié avec succès.')
            return redirect('reports:detail', pk=report.pk)
    else:
        form = ReportForm(instance=report)
    
    return render(request, 'reports/update_report.html', {
        'form': form,
        'report': report
    })
