# Generated by Django 5.0.1 on 2024-01-21 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_alter_blog_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'verbose_name': 'Запись', 'verbose_name_plural': 'Записи'},
        ),
    ]
