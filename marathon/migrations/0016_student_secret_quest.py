# Generated by Django 3.0.5 on 2020-04-21 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marathon', '0015_auto_20200419_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='secret_quest',
            field=models.BooleanField(default=False),
        ),
    ]
