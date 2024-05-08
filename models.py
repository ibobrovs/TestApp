from django.db import models
from .resources import POSITIONS
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse



class Author(models.Model):
    rating = models.FloatField(default=0.0, max=10)
    users = models.OneToOneField("User", on_delete=models.CASCADE)

    def update_rating(self):
        post_rating = sum(post.rating for post in self.post_set.all()) * 3
        comment_rating = sum(comment.rating for comment in self.comment_set.all())
        post_comment_rating = sum(comment.rating for post in self.post_set.all() for comment in post.comment_set.all())
        self.rating = post_rating + comment_rating + post_comment_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    ARTICLE = 'article'
    NEWS = 'news'
    POST_CHOICE = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]
    post_type = models.CharField(max_length=20, choices=POST_CHOICE)
    time_in = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    post_rating = models.IntegerField(max_length=10)

    def like(self):
        self.rating += 1
        self.save()
    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.text) > 124 return self.text[:124] + '...', else self.text




class PostCategory(models.Model):
    post = models.OneToManyField(Post, on_delete=models.CASCADE)
    category = models.OneToManyField(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.OnetoMany(Post, on_delete=models.CASCADE)
    user = models.OnetoMany(User, on_delete=models.CASCADE)
    text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(max_length=10)

    def like(self):
        self.rating += 1
        self.save()
    def dislike(self):
        self.rating -= 1
        self.save()


# class Order(models.Model):
#     time_in = models.DateTimeField(auto_now_add=True)
#     time_out = models.DateTimeField(null=True)
#     cost = models.FloatField(default=0.0)
#     take_away = models.BooleanField(default=False)
#     complete = models.BooleanField(default=False)
#
#     staff = models.ForeignKey("Staff", on_delete=models.CASCADE)
#     products = models.ManyToManyField("Product", through='ProductOrder')
#
#     def finish_order(self):
#         self.time_out = datetime.now()
#         self.complete = True
#         self.save()
#
#     def get_duration(self):
#         if self.complete:
#             return(self.time_out - self.time_in).total_seconds()
#         else:
#             return(datetime.now() - self.time_in).total_seconds()
#
# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     price = models.FloatField(default=0.0)
#
#     def get_absolute_url(self):
#         return reverse('product_detail', args=[str(self.id)])
#
#
# class Staff(models.Model):
#     director = 'DI'
#     admin = 'AD'
#     cook = 'CO'
#     cashier = 'CA'
#     cleaner = 'CL'
#
#     full_name = models.CharField(max_length=255)
#     position = models.CharField(max_length=2, choices=POSITIONS, default='DI')
#     labor_contract = models.IntegerField()
#
#
# class ProductOrder(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     _amount = models.IntegerField(default=1, db_column='amount')
#
#     def product_sum(self):
#         return self.product.price * self.amount
#
#
#     @property
#     def amount(self):
#         return self.amount
#
#     @amount.setter
#     def amount(self, value):
#         self._amount = int(value) if value >= 0 else 0
#         self.save()
