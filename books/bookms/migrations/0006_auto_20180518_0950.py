# Generated by Django 2.0.4 on 2018-05-18 01:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookms', '0005_auto_20180517_2241'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='分类')),
            ],
        ),
        migrations.AddField(
            model_name='books',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bookms.Categories'),
        ),
        migrations.AddField(
            model_name='readers',
            name='latest_borrowed_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bookms.Categories'),
        ),
    ]
