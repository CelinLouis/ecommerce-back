from magasin_bd.models.produit import Produit
from magasin_bd.models.achat import Achat
from rest_framework import serializers
from magasin_bd.serializers.produit import ProduitSerializer


class AchatSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Achat
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super(AchatSerializer, self).to_representation(instance)
        produit = Produit.objects.get(id=data["produit"])
        data["produit"] = ProduitSerializer(produit).data
        return data


class AchatPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Achat
        fields = ('id','produit','quantite')