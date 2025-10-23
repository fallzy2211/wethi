from django.contrib.auth.models import AbstractUser
from django.db import models

Devise = (
       ('CFA', 'CFA'),
       ('EUR', 'EUR'),
       ('USD', 'USD'),
       ('GBP', 'GBP'),
       ('YEN', 'YEN'),
       ('CHF','CHF'),
   )
Devises = (
       ('CFA', 'CFA'),
   )

Type = (
       ('Vente', 'Vente'),
       ('Achat', 'Achat'),
   )



class User(AbstractUser):
    TYPE_CHOICES = [
        ('particulier', 'Particulier'),
        ('cambiste', 'Cambiste'),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    credits = models.PositiveIntegerField(default=0)

    piece_identite = models.ImageField(upload_to='pieces_identite/', blank=True, null=True)
    numero_agrement = models.CharField(max_length=100, blank=True, null=True)
    document_agrement = models.ImageField(upload_to='documents_agrement/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_type_display()})"


class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offers")
    ma_devise = models.CharField(choices=Devise,max_length=5)
    devise_souhaitee = models.CharField(choices=Devise,max_length=5)
    taux_souhaite = models.IntegerField(blank=True)
    quantite = models.IntegerField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('disponible', 'Disponible'),
        ('reservee', 'Réservée'),
        ('completee', 'Complétée'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponible')
    reserved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="reserved_offers")

    def __str__(self):
        return f"{self.user} échange {self.taux_souhaite} {self.ma_devise} → {self.devise_souhaitee}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.receiver} : {self.content[:30]}"
