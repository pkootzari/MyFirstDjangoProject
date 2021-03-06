# Generated by Django 3.0.3 on 2020-06-23 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companymodels', '0002_auto_20200623_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cost',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='factor',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='companymodels.Invoice'),
        ),
        migrations.AlterField(
            model_name='order',
            name='services',
            field=models.ManyToManyField(blank=True, null=True, related_name='orders', to='companymodels.Service'),
        ),
    ]
