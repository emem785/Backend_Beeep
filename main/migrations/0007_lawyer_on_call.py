# Generated by Django 3.0.2 on 2020-10-08 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20201003_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawyer',
            name='on_call',
            field=models.BooleanField(default=False),
        ),
    ]