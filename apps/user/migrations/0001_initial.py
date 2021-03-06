# Generated by Django 2.0.4 on 2018-05-10 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(db_index=True, max_length=64, unique=True)),
                ('truename', models.CharField(max_length=64)),
                ('department', models.IntegerField()),
                ('phone', models.CharField(max_length=20)),
                ('areacode', models.IntegerField())
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('province', models.CharField(max_length=16)),
                ('role', models.IntegerField()),
            ],
            options={
                'db_table': 'departments',
            },
        ),
    ]
