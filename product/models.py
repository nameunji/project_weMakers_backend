from django.db import models

class ProductMainCategories(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'product_main_categories'


class ProductSubCategories(models.Model):
    name             = models.CharField(max_length = 50)
    main_category    = models.ForeignKey(ProductMainCategories, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_sub_categories'


class Brands(models.Model):
    main_category    = models.ForeignKey(ProductMainCategories, on_delete=models.CASCADE)
    name             = models.CharField(max_length = 100)
    logo_image       = models.URLField(max_length = 2000, null=True)
    info             = models.CharField(max_length = 1000, null=True)
    detail_image     = models.URLField(max_length = 2000, null=True)

    class Meta:
        db_table = 'brands'


class Products(models.Model):
    main_category    = models.ForeignKey(ProductMainCategories, on_delete=models.CASCADE)
    sub_category     = models.ForeignKey(ProductSubCategories, on_delete=models.CASCADE)
    brand            = models.ForeignKey(Brands, on_delete=models.CASCADE)
    name             = models.CharField(max_length = 100)
    price            = models.DecimalField(max_digits=11, decimal_places=2)
    minimum_count    = models.SmallIntegerField()
    maximum_count    = models.SmallIntegerField()
    start_date       = models.DateTimeField()
    end_date         = models.DateTimeField()
    delivery_date    = models.DateField()
    delivery_charge  = models.DecimalField(max_digits=9, decimal_places=2)
    detail_content   = models.TextField()
    info_detail      = models.TextField()

    class Meta:
        db_table = 'products'


class ProductInfo(models.Model):
    product      = models.ForeignKey(Products, on_delete=models.CASCADE)
    artist       = models.CharField(max_length = 50, null=True)
    main_text    = models.CharField(max_length = 1000, null=True)
    md_name      = models.CharField(max_length = 50, null=True)
    main_image   = models.URLField(max_length = 2000, null=True)
    new_image    = models.URLField(max_length = 2000, null=True)
    search_image = models.URLField(max_length = 2000, null=True)

    class Meta:
        db_table = 'product_info'


class ProductSubImages(models.Model):
    product    = models.ForeignKey(Products, on_delete=models.CASCADE)
    sub_image  = models.URLField(max_length = 2000, null=True)

    class Meta:
        db_table = 'product_sub_images'


class ProductOptionTitles(models.Model):
    product      = models.ForeignKey(Products, on_delete=models.CASCADE)
    option_title = models.CharField(max_length = 100, null=True)
    
    class Meta:
        db_table = 'product_option_titles'


class ProductOptionDetails(models.Model):
    product_option_title = models.ForeignKey(ProductOptionTitles, on_delete=models.CASCADE)
    option_detail        = models.CharField(max_length = 100, null=True)

    class Meta:
        db_table = 'product_option_details'



