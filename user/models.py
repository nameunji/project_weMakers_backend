from django.db import models

class Users(models.Model):
    email    = models.CharField(max_length = 70, unique = True)
    password = models.CharField(max_length = 300)
    nickname = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'users'    
