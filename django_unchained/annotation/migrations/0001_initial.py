# Generated by Django 3.0.6 on 2020-06-10 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_sentences', models.IntegerField(default=0)),
                ('number_of_labeled_sentences', models.IntegerField(default=0)),
                ('percentage_labeled', models.IntegerField(default=0)),
                ('assignee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Corpus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, unique=True)),
                ('tag_line', models.CharField(max_length=500, unique=True)),
                ('description', models.CharField(max_length=10000, unique=True)),
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
            name='ExampleSentence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500, unique=True)),
                ('corpus', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='annotation.Corpus')),
                ('entities', models.ManyToManyField(to='annotation.Entity')),
            ],
        ),
        migrations.CreateModel(
            name='TestRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_example_sentences', models.IntegerField(default=0)),
                ('corpus', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='annotation.Corpus')),
            ],
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500, unique=True)),
                ('corpus', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='annotation.Corpus')),
                ('entities', models.ManyToManyField(to='annotation.Entity')),
            ],
        ),
        migrations.CreateModel(
            name='RelationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, unique=True)),
                ('description', models.CharField(max_length=1000, unique=True)),
                ('example1', models.CharField(max_length=1000, unique=True)),
                ('example2', models.CharField(max_length=1000, unique=True)),
                ('example3', models.CharField(max_length=1000, unique=True)),
                ('example4', models.CharField(max_length=1000, unique=True)),
                ('example5', models.CharField(max_length=1000, unique=True)),
                ('corpus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='annotation.Corpus')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('labeled', models.BooleanField(default=False)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='annotation.Batch')),
                ('sentence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='annotation.Sentence')),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='entity1', to='annotation.Entity')),
                ('entity2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='entity2', to='annotation.Entity')),
                ('relation_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='annotation.RelationType')),
                ('sentence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='annotation.Sentence')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GoldLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('example_sentence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='annotation.ExampleSentence')),
                ('goldentity1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='goldentity1', to='annotation.Entity')),
                ('goldentity2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='goldentity2', to='annotation.Entity')),
                ('goldrelation_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='annotation.RelationType')),
            ],
        ),
        migrations.AddField(
            model_name='examplesentence',
            name='testrun',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='annotation.TestRun'),
        ),
        migrations.AddField(
            model_name='batch',
            name='corpus',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='annotation.Corpus'),
        ),
        migrations.AddField(
            model_name='batch',
            name='sentences',
            field=models.ManyToManyField(through='annotation.Membership', to='annotation.Sentence'),
        ),
    ]
