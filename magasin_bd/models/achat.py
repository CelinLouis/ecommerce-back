from django.db import models
from magasin_bd.models.produit import Produit


class Achat(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name="par_produit")
    quantite = models.IntegerField(default=0, blank=False, null=False)
    prix_total = models.FloatField(default=0, blank=False, null=False)
    date_achat = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.produit.nom + ' ' + str(self.date_achat) 