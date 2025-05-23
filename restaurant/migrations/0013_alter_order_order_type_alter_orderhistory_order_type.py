# Generated by Django 5.1.4 on 2024-12-31 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0012_alter_order_order_type_alter_orderhistory_order_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_type',
            field=models.CharField(choices=[('table', 'Table'), ('takeaway', 'Takeaway'), ('delivery', 'Delivery')], max_length=10),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='order_type',
            field=models.CharField(choices=[('table', 'Table'), ('takeaway', 'Takeaway'), ('delivery', 'Delivery')], default='dine_in', max_length=20),
        ),
    ]
