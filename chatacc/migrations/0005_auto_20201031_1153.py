# Generated by Django 3.1.2 on 2020-10-31 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatacc', '0004_auto_20201030_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='external_id',
            field=models.PositiveIntegerField(unique=True, verbose_name='ID of the user at the social network'),
        ),
    ]
