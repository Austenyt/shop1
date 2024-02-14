# Generated by Django 4.2 on 2024-02-11 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0016_alter_product_is_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': [('can_unpublish_product', 'Can unpublish product'), ('can_change_product_description', 'Can change product description'), ('can_change_product_category', 'Can change product category')], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
    ]