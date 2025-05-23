# Generated by Django 5.1.4 on 2024-12-27 17:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_payment_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={},
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='subtotal',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_date',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='table',
            name='qr_code',
        ),
        migrations.AddField(
            model_name='payment',
            name='date_edited',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='edited_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='table',
            name='capacity',
            field=models.PositiveIntegerField(default=4),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='image',
            field=models.ImageField(blank=True, upload_to='menu_images/'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='preparation_area',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_type',
            field=models.CharField(choices=[('dine_in', 'Dine In'), ('takeaway', 'Takeaway'), ('delivery', 'Delivery')], default='dine_in', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('cash', 'Cash'), ('card', 'Card'), ('upi', 'UPI')], default='cash', max_length=20),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='order_type',
            field=models.CharField(choices=[('dine_in', 'Dine In'), ('takeaway', 'Takeaway'), ('delivery', 'Delivery')], default='dine_in', max_length=20),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.menuitem'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='payment',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.order'),
        ),
        migrations.AlterField(
            model_name='table',
            name='number',
            field=models.PositiveIntegerField(unique=True),
        ),
        migrations.CreateModel(
            name='OrderHistoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.menuitem')),
                ('order_history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='restaurant.orderhistory')),
            ],
        ),
    ]
