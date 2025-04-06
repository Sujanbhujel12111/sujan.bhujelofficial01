# Generated by Django 5.1.4 on 2025-01-05 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0016_alter_orderhistory_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderhistory',
            name='payment_status',
        ),
        migrations.AddField(
            model_name='orderhistory',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Cash'), ('card', 'Card'), ('fonepay', 'Fonepay'), ('bank', 'Bank'), ('khalti', 'Khalti'), ('ipay', 'Ipay'), ('prabhu', 'Prabhu'), ('esewa', 'Esewa'), ('imepay', 'Imepay'), ('connectips', 'Connectips'), ('sct', 'SCT'), ('qr_code', 'QR Code'), ('other', 'Other')], default='cash', max_length=20),
        ),
    ]
