# Generated by Django 5.0.1 on 2024-02-01 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0009_version_version_number_alter_version_current_version_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='version',
            old_name='current_version',
            new_name='is_active',
        ),
    ]