# Generated by Django 5.0.4 on 2024-04-25 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wander', '0012_alter_guide_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitplan',
            name='modeOfPayment',
            field=models.CharField(choices=[('Cash', 'Cash'), ('Online', 'Online')], default='', max_length=10),
        ),
    ]