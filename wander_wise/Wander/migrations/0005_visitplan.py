# Generated by Django 5.0.4 on 2024-04-20 11:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wander', '0004_alter_guide_govtidtype'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(choices=[('1', 'Lucknow')], max_length=100)),
                ('place', models.CharField(choices=[('1', 'Lucknow Zoo'), ('2', 'Bara Imambara'), ('3', 'Chota Imambara'), ('4', 'Rumi Darwaza')], max_length=100)),
                ('from_date_time', models.DateTimeField()),
                ('to_date_time', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
