# Generated by Django 4.0.1 on 2022-01-10 02:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tinkerplants', '0002_remove_implant_metatype_cluster_hival_cluster_loval_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='implant',
            name='type',
        ),
    ]
