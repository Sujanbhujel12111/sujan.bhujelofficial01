# Generated by Django 5.1.4 on 2024-12-27 19:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0007_remove_order_created_at_remove_order_updated_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='completed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='completed_orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderhistory',
            name='completed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='completed_order_histories', to=settings.AUTH_USER_MODEL),
        ),
    ]
