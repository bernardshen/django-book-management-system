# Generated by Django 2.0.4 on 2018-05-18 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookms', '0009_books_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratings',
            name='comment',
            field=models.TextField(default=None, null=True, verbose_name='评论'),
        ),
    ]
