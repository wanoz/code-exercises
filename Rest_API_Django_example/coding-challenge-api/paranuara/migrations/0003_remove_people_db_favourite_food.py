# Generated by Django 2.0.2 on 2018-03-18 05:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paranuara', '0002_auto_20180318_0018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='people_db',
            name='favourite_food',
        ),
    ]
