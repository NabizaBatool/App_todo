# Generated by Django 2.2.12 on 2022-08-30 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0006_auto_20220830_0612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='complete',
            field=models.BooleanField(null=True),
        ),
    ]
