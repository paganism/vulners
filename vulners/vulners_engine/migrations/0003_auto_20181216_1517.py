# Generated by Django 2.1.4 on 2018-12-16 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vulners_engine', '0002_auto_20181215_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vulner',
            name='published',
            field=models.DateTimeField(),
        ),
    ]