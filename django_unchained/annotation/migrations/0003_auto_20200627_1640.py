# Generated by Django 3.0.6 on 2020-06-27 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0002_entity_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='type',
            field=models.CharField(default=' ', max_length=500),
        ),
    ]