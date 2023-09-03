from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    name_readonly = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField()
    max_crowd = models.PositiveIntegerField(default=1)
    current_crowd = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Feedback(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    feedback = models.TextField()
    rating = models.PositiveIntegerField(default=0)
    is_feedback_positive = models.BooleanField(default=True)

    def __str__(self):
        return f"Feedback for {self.product} at {self.shop}"
