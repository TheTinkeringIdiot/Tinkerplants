# Generated by Django 4.2.6 on 2024-03-01 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinkertools', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='action',
            field=models.IntegerField(null=True),
        ),
    ]
