# Generated by Django 5.1 on 2025-04-19 04:12

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('discount_type', models.CharField(choices=[('percentage', 'Percentage'), ('fixed', 'Fixed Amount')], max_length=10)),
                ('value', models.DecimalField(decimal_places=2, max_digits=6)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductsCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, unique=True)),
                ('friendly_name', models.CharField(blank=True, max_length=254, null=True)),
            ],
            options={
                'verbose_name_plural': 'Product Categories',
            },
        ),
        migrations.CreateModel(
            name='HennaProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('name', models.CharField(max_length=254, unique=True)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rating', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('stock_quantity', models.PositiveIntegerField(default=0)),
                ('is_available', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('image_url', models.URLField(blank=True, max_length=1024, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('discounts', models.ManyToManyField(blank=True, to='products.discount')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.productscategory')),
            ],
        ),
    ]
