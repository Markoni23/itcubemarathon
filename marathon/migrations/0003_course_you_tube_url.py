# Generated by Django 3.0.5 on 2020-04-16 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marathon', '0002_auto_20200412_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='you_tube_url',
            field=models.URLField(default=''),
        ),
    ]
