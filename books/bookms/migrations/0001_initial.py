# Generated by Django 2.0.4 on 2018-04-23 15:05

import datetime
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
            name='Authors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='姓名')),
                ('sex', models.IntegerField(choices=[(0, '男'), (1, '女')])),
                ('birthday', models.DateField(null=True, verbose_name='生日')),
                ('date_death', models.DateField(null=True)),
                ('nation', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('name', models.CharField(max_length=128, verbose_name='书名')),
                ('inc_date', models.DateField(verbose_name='入库日期')),
                ('isbn', models.CharField(max_length=128, primary_key=True, serialize=False, unique=True, verbose_name='索书号')),
                ('num_copies', models.IntegerField(default=1, verbose_name='副本')),
                ('num_lend', models.IntegerField(default=0, verbose_name='借出数')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookms.Authors')),
            ],
        ),
        migrations.CreateModel(
            name='Borrows',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('repeat', models.IntegerField(default=0)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookms.Books')),
            ],
        ),
        migrations.CreateModel(
            name='Publishers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='出版社')),
            ],
        ),
        migrations.CreateModel(
            name='Readers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reader_identity', models.IntegerField(verbose_name='读者证编号')),
                ('reg_date', models.DateField()),
                ('age', models.IntegerField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='borrows',
            name='reader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookms.Readers'),
        ),
        migrations.AddField(
            model_name='books',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookms.Publishers'),
        ),
    ]
