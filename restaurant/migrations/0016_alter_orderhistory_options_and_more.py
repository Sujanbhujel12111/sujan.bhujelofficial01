# Generated by Django 5.1.4 on 2024-12-31 11:17

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0015_alter_category_options_alter_menuitem_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderhistory',
            options={},
        ),
        migrations.RemoveField(
            model_name='orderhistory',
            name='delivery_charge',
        ),
        migrations.RemoveField(
            model_name='orderhistory',
            name='payment_details',
        ),
        migrations.RemoveField(
            model_name='orderhistoryitem',
            name='item_description',
        ),
        migrations.RemoveField(
            model_name='orderhistoryitem',
            name='item_name',
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_charge',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Delivery charge for delivery orders', max_digits=10),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='completed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='completed_order_histories', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='customer_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='customer_phone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='order_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='order_type',
            field=models.CharField(choices=[('table', 'Table'), ('takeaway', 'Takeaway'), ('delivery', 'Delivery')], default='dine_in', max_length=20),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='payment_status',
            field=models.CharField(choices=[('cash', 'Cash'), ('card', 'Card'), ('fonepay', 'Fonepay'), ('bank', 'Bank'), ('khalti', 'Khalti'), ('ipay', 'Ipay'), ('prabhu', 'Prabhu'), ('esewa', 'Esewa'), ('imepay', 'Imepay'), ('connectips', 'Connectips'), ('sct', 'SCT'), ('qr_code', 'QR Code'), ('other', 'Other')], default='completed', max_length=20),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='special_notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending Confirmation'), ('confirmed', 'Confirmed'), ('preparing', 'Preparing'), ('ready', 'Ready'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='completed', max_length=20),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='orderhistoryitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.menuitem'),
        ),
    ]
