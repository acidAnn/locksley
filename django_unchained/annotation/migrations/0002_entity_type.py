# Generated by Django 3.0.6 on 2020-06-27 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='type',
            field=models.CharField(default='', max_length=500),
        ),
    ]
