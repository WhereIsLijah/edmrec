# Generated by Django 5.0.6 on 2024-11-23 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EDMRecData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('url', models.URLField()),
                ('size', models.CharField(max_length=50)),
                ('format', models.CharField(max_length=50)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('tfidf_embeddings', models.BinaryField()),
                ('bert_embeddings', models.BinaryField()),
                ('source', models.CharField(max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='TestModel',
        ),
    ]
