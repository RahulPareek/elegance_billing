# Generated by Django 2.1 on 2018-11-08 05:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0002_auto_20181108_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentdetails',
            name='bill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill.Bill'),
        ),
    ]
