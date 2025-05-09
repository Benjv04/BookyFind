# Generated by Django 5.1.7 on 2025-05-03 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='libro',
            name='descripcion',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='libro',
            name='editorial',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='libro',
            name='fecha_publicacion',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='libro',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
