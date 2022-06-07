from django.db import models


class Produit(models.Model):
    nom = models.CharField(max_length=20, blank=False, null=False)
    prix = models.FloatField(default=0, blank=False, null=False)
    quantite = models.IntegerField(default=0, blank=False, null=False)
    date_modification = models.DateTimeField(auto_now_add=False, auto_now=True)
    date_creaction = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    def __str__(self):
        return self.nom + ' ' + str(self.date_modification) + ' ' + str(self.date_creaction)