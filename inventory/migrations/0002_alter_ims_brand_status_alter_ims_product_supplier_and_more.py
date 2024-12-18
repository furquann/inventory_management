# Generated by Django 5.0.1 on 2024-02-07 18:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ims_brand',
            name='status',
            field=models.BooleanField(choices=[(True, 'Active'), (False, 'Inactive')], default=True),
        ),
        migrations.AlterField(
            model_name='ims_product',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.ims_supplier'),
        ),
        migrations.AlterField(
            model_name='ims_supplier',
            name='status',
            field=models.BooleanField(choices=[(True, 'Active'), (False, 'Inactive')], default=True),
        ),
    ]
