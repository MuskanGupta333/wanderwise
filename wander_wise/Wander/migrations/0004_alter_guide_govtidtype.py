# Generated by Django 5.0.4 on 2024-04-20 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wander', '0003_guide'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guide',
            name='govtIdType',
            field=models.CharField(choices=[('PAN Card', 'PAN Card'), ('Aadhar Card', 'Aadhar Card')], max_length=20),
        ),
    ]
