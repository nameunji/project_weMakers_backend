from django.db import models

class ProductMainCategories(models.Model):
    name = models.CharField(max_length = 50)
    class Meta:
        db_table = 'product_main_categories'


class ProductSubCategories(models.Model):
    name             = models.CharField(max_length = 50)
    main_category_id = models.ForeignKey(ProductMainCategories, on_delete=models.CASCADE)
    class Meta:
        db_table = 'product_sub_categories'


class Brands(models.Model):
    main_category_id = models.ForeignKey(ProductMainCategories, on_delete=models.CASCADE)
    name             = models.CharField(max_length = 100)
    logo_image       = models.URLField(max_length = 2000, null=True)
    info             = models.CharField(max_length = 1000, null=True)
    detail_image     = models.URLField(max_length = 2000, null=True)
    class Meta:
        db_table = 'brands'
