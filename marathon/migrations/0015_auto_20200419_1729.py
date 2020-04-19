# Generated by Django 3.0.5 on 2020-04-19 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('marathon', '0014_auto_20200419_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecomment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]
