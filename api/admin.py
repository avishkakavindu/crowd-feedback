from django.contrib import admin
from .models import Shop, Product, Feedback


class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('shop', 'product', 'rating', 'is_feedback_positive')


# Register models with admin classes
admin.site.register(Shop, ShopAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Feedback, FeedbackAdmin)
