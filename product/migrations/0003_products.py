# Generated by Django 3.0.1 on 2019-12-30 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20191230_1641'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=11)),
                ('minimum_count', models.SmallIntegerField()),
                ('maximum_count', models.SmallIntegerField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('delivery_date', models.DateField()),
                ('delivery_charge', models.DecimalField(decimal_places=2, max_digits=9)),
                ('detail_content', models.TextField()),
                ('info_detail', models.TextField()),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Brands')),
                ('main_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.ProductMainCategories')),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.ProductSubCategories')),
            ],
            options={
                'db_table': 'products',
            },
        ),
    ]
