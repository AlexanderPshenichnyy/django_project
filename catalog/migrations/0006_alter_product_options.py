# Generated by Django 4.2.7 on 2024-01-13 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_product_is_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': [('set_published_status', 'Can publish products')], 'verbose_name': 'Product', 'verbose_name_plural': 'Produts'},
        ),
    ]