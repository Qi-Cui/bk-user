# Generated by Django 3.2.25 on 2024-08-01 07:51

import bkuser.utils.uuid
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('data_source', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NaturalUser',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.CharField(default=bkuser.utils.uuid.generate_uuid, max_length=128, primary_key=True, serialize=False, verbose_name='自然人标识')),
                ('full_name', models.CharField(max_length=128, verbose_name='姓名')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DataSourceUserNaturalUserRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('data_source_user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='data_source.datasourceuser')),
                ('natural_user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='natural_user.naturaluser')),
            ],
            options={
                'ordering': ['id'],
                'unique_together': {('data_source_user', 'natural_user')},
            },
        ),
    ]
