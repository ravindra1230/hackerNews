# Generated by Django 2.2.3 on 2019-07-18 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='comments',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='article',
            name='hacker_news_url',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='article',
            name='posted_on',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='article',
            name='upvotes',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='article',
            name='url',
            field=models.CharField(max_length=200),
        ),
    ]