# Generated by Django 3.0 on 2022-09-05 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NoteTake', '0002_auto_20220903_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='userid',
            field=models.CharField(default=-1, max_length=1000),
            preserve_default=False,
        ),
    ]