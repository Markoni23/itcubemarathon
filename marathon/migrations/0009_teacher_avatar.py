# Generated by Django 3.0.5 on 2020-04-17 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marathon', '0008_auto_20200417_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]