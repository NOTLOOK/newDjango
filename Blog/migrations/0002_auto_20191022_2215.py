# Generated by Django 2.1 on 2019-10-22 14:15

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='body',
            field=DjangoUeditor.models.UEditorField(blank=True, verbose_name='内容'),
        ),
    ]