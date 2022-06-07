from magasin_bd.models.produit import Produit
from magasin_bd.models.achat import Achat
from rest_framework import serializers 
from rest_framework.fields import SerializerMethodField
from django.db.models.aggregates import Sum


class ProduitSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Produit
        fields = '__all__'


class AchatSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Achat
        fields = ('id','quantite','prix_total','date_achat')


class ParProduitSerializer(serializers.ModelSerializer):
    par_produit = SerializerMethodField('get_achat')

    class Meta:
        model = Produit
        fields = '__all__'


    def to_representation(self, instance):
        data = super(ParProduitSerializer, self).to_representation(instance)
        gain_total = 0
        gain = Achat.objects.filter(produit=data['id']).values('produit').aggregate(gain_total=Sum('prix_total'))
        if gain is not None:
            gain_total = gain["gain_total"] or 0
        data["gain_total"]=gain_total
        return data

        
    def get_achat(self, id):
        achat = Achat.objects.filter(produit=id).order_by("-date_achat")
        return AchatSerializer(achat, many=True).data


class ProduitQuantiteNewSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Produit
        fields = ('id','quantite')