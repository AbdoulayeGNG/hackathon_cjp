from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Utilisateur(AbstractUser):
    ROLES = (
        ('citoyen', 'Citoyen'),
        ('touriste', 'Touriste'),
        ('admin', 'Administrateur'),
    )

    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=10, choices=ROLES, default='citoyen')
    phone = models.CharField(max_length=15, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    date_naissance = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    
    # Champ pour la vérification OTP
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('utilisateur')
        verbose_name_plural = _('utilisateurs')

    def __str__(self):
        return self.email
