# Generated by Django 4.0 on 2022-10-08 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0016_rename_shippingaddress_deliveryaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]