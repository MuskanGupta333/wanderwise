# Generated by Django 5.0.4 on 2024-04-15 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wander', '0012_guide_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guide',
            name='quiz_score',
            field=models.IntegerField(default=0),
        ),
    ]
