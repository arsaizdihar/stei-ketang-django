# Generated by Django 3.2.9 on 2021-11-18 03:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_changepasswordkey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changepasswordkey',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='change', to=settings.AUTH_USER_MODEL),
        ),
    ]
