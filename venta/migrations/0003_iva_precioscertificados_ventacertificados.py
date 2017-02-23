# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 15:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('venta', '0002_delete_sale'),
    ]

    operations = [
        migrations.CreateModel(
            name='Iva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precioiva', models.DecimalField(decimal_places=2, max_digits=5)),
                ('creado', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='PreciosCertificados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preciocertificado', models.DecimalField(decimal_places=2, max_digits=5)),
                ('creado', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='VentaCertificados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asociacion', models.CharField(max_length=100)),
                ('preciocertificado', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cantidad', models.IntegerField()),
                ('tipocambio', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ivaporcentaje', models.DecimalField(decimal_places=2, max_digits=4)),
                ('monto', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('montoiva', models.DecimalField(decimal_places=2, max_digits=9)),
                ('total', models.DecimalField(decimal_places=2, max_digits=9)),
                ('creado', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
    ]
