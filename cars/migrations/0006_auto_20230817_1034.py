# Generated by Django 3.2.20 on 2023-08-17 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0005_post_reply'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reply',
            name='author',
        ),
        migrations.RemoveField(
            model_name='reply',
            name='post',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='Reply',
        ),
    ]