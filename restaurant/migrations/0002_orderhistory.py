# Generated by Django 5.1.4 on 2024-12-26 16:41

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('customer_name', models.CharField(blank=True, max_length=100)),
                ('customer_phone', models.CharField(blank=True, max_length=20)),
                ('order_type', models.CharField(choices=[('dine_in', 'Dine In'), ('takeaway', 'Take Away')], default='dine_in', max_length=20)),
                ('status', models.CharField(choices=[('pending', 'Pending Confirmation'), ('confirmed', 'Confirmed'), ('preparing', 'Preparing'), ('ready', 'Ready'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='completed', max_length=20)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed')], default='completed', max_length=20)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('special_notes', models.TextField(blank=True)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('table', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.table')),
            ],
        ),
    ]
