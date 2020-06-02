# Generated by Django 3.0.6 on 2020-06-02 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0004_auto_20200531_2042'),
    ]

    operations = [
        migrations.CreateModel(
            name='Corpus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='RelationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, unique=True)),
                ('corpus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='annotation.Corpus')),
            ],
        ),
        migrations.AddField(
            model_name='batch',
            name='corpus',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='annotation.Corpus'),
        ),
        migrations.AddField(
            model_name='label',
            name='object',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='object', to='annotation.Entity'),
        ),
        migrations.AddField(
            model_name='label',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subject', to='annotation.Entity'),
        ),
        migrations.AddField(
            model_name='sentence',
            name='entities',
            field=models.ManyToManyField(to='annotation.Entity'),
        ),
        migrations.AlterField(
            model_name='label',
            name='relation_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='annotation.RelationType'),
        ),
    ]
