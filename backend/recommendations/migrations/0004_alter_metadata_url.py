# Generated by Django 5.0.6 on 2024-11-23 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0003_embedding_metadata_query_queryresult_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metadata',
            name='url',
            field=models.URLField(unique=True),
        ),
    ]