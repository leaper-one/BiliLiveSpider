# Generated by Django 3.2.12 on 2022-03-19 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0002_auto_20220319_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='naomi',
            name='uid',
            field=models.CharField(max_length=100),
        ),
    ]
