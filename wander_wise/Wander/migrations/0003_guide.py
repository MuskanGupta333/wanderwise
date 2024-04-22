# Generated by Django 5.0.4 on 2024-04-20 08:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wander', '0002_delete_guide'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('languages_known', models.CharField(default='', max_length=100)),
                ('places_known', models.CharField(default='', max_length=100)),
                ('govtIdType', models.CharField(choices=[('PAN Card', 'PAN Card'), ('Aadhar Card', 'Aadhar Card')], default='', max_length=20)),
                ('govt_id', models.CharField(default='', max_length=100)),
                ('quiz_score', models.IntegerField(default=0)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='guide', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]