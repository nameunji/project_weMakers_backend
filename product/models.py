from django.db   import models
from user.models import Users

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

    order            = models.ManyToManyField(Users, through='Orders')
    review           = models.ManyToManyField(Users, through='ProductReviews', related_name='product_reviews_set')
    question         = models.ManyToManyField(Users, through='ProductQuestions', related_name='product_questions_set')
    user_like        = models.ManyToManyField(Users, through='UserLikeProducts', related_name='user_like_products_set')

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
    price                = models.DecimalField(max_digits=11, decimal_places=2, null=True)

    class Meta:
        db_table = 'product_option_details'


class OrderStatus(models.Model):
    status = models.CharField(max_length = 50)

    class Meta:
        db_table = 'order_status'


class Orders(models.Model):
    product         = models.ForeignKey(Products, on_delete=models.CASCADE)
    user            = models.ForeignKey(Users, on_delete=models.CASCADE)
    order_status    = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)
    order_number    = models.IntegerField(unique = True)
    quantity        = models.SmallIntegerField()
    total_amount    = models.DecimalField(max_digits=11, decimal_places=2)
    delivery_number = models.CharField(max_length = 50, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'


class ProductReviews(models.Model):
    product    = models.ForeignKey(Products, on_delete=models.CASCADE)
    user       = models.ForeignKey(Users, on_delete=models.CASCADE)
    content    = models.CharField(max_length=500)
    image      = models.URLField(max_length=2000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    grade      = models.SmallIntegerField()

    class Meta:
        db_table = 'product_reviews'


class ProductQuestions(models.Model):
    product    = models.ForeignKey(Products, on_delete=models.CASCADE)
    user       = models.ForeignKey(Users, on_delete=models.CASCADE)
    content    = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        db_table = 'product_questions'


class ProductAnswers(models.Model):
    question    = models.ForeignKey(ProductQuestions, on_delete=models.CASCADE)
    content     = models.CharField(max_length = 1000)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_answers'


class UserLikeProducts(models.Model):
    user    = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_like_products'



