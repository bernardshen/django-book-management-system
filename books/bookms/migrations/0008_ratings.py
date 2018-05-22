# Generated by Django 2.0.4 on 2018-05-18 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookms', '0007_readers_forbid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(default=None, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookms.Books')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookms.Readers')),
            ],
        ),
    ]