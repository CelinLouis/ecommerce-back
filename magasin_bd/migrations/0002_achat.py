# Generated by Django 3.2.13 on 2022-06-06 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('magasin_bd', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.IntegerField(default=0)),
                ('prix_total', models.FloatField(default=0)),
                ('date_achat', models.DateTimeField(auto_now_add=True)),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='par_produit', to='magasin_bd.produit')),
            ],
        ),
    ]