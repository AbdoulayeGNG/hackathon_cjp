from django.db import models
from django.utils.translation import gettext_lazy as _
from utilisateurs.models import Utilisateur

class Report(models.Model):
    CATEGORY_CHOICES = [
        ('road', 'Route endommagée'),
        ('light', 'Éclairage public'),
        ('trash', 'Déchets'),
        ('water', 'Problème d\'eau'),
        ('other', 'Autre')
    ]

    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('in_progress', 'En cours'),
        ('resolved', 'Résolu'),
    ]

    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, verbose_name=_('utilisateur'))
    title = models.CharField(_('titre'), max_length=255)
    category = models.CharField(_('catégorie'), max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(_('description'))
    image = models.ImageField(_('image'), upload_to='reports/', blank=True, null=True)
    location_lat = models.FloatField(_('latitude'))
    location_lng = models.FloatField(_('longitude'))
    address = models.CharField(_('adresse'), max_length=255)
    status = models.CharField(_('statut'), max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(_('date de création'), auto_now_add=True)
    updated_at = models.DateTimeField(_('dernière modification'), auto_now=True)

    class Meta:
        verbose_name = _('signalement')
        verbose_name_plural = _('signalements')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_status_color(self):
        return {
            'pending': 'warning',
            'in_progress': 'info',
            'resolved': 'success'
        }.get(self.status, 'secondary')
