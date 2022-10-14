# Generated by Django 4.1 on 2022-10-11 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0018_remove_orderitem_order_orderitem_orders'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='orders',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ManyToManyField(to='project.order'),
        ),
    ]
